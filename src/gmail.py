import os
import pickle
import base64
import io
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pypdf import PdfReader
from PIL import Image
import pytesseract

# gmail api scopes - read only access
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class Gmail:
    def __init__(self):
        self.service = None

    def auth(self):
        """authenticate with gmail api"""
        try:
            creds = None

            # where access/refresh tokens live
            if os.path.exists("token.pickle"):
                with open("token.pickle", "rb") as t:
                    creds = pickle.load(t)

            # if not valid creds - login
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    credentials_path = os.path.join(
                        os.path.dirname(__file__), "credentials.json"
                    )
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, SCOPES
                    )
                    creds = flow.run_local_server()

                    # save creds for next time
                    with open("token.pickle", "wb") as t:
                        pickle.dump(creds, t)

            self.service = build("gmail", "v1", credentials=creds)
            return self.service
        except FileNotFoundError:
            raise RuntimeError("create credentials.json from template")
        except Exception as e:
            raise RuntimeError(f"failed auth: {e}")

    def test(self):
        """test gmail api connection"""
        try:
            if not self.service:
                self.auth()
            self.service.users().getProfile(userId="me").execute()
        except Exception as e:
            raise RuntimeError(f"failed connection test: {e}")

    def fetch(self, max_results=20):
        """fetch emails from gmail"""
        try:
            if not self.service:
                self.auth()

            # get list of messages
            result = (
                self.service.users()
                .messages()
                .list(userId="me", maxResults=max_results)
                .execute()
            )
            messages = result.get("messages", [])

            emails = []
            for i, message in enumerate(messages, 1):
                print(f"Processing email {i}/{len(messages)}...")
                msg = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=message["id"], format="full")
                    .execute()
                )
                emails.append(self._parse_message(msg))

            return emails
        except Exception as e:
            raise RuntimeError(f"failed email fetch: {e}")

    def _parse_message(self, message):
        """parse gmail message into dict"""
        try:
            headers = message["payload"]["headers"]
            header_map = {h["name"]: h["value"] for h in headers}

            body_text, content, attachments = self._parse_payload(
                message["payload"], message["id"]
            )

            return {
                "id": message["id"],
                "thread_id": message["threadId"],
                "subject": header_map.get("Subject", ""),
                "sender": header_map.get("From", ""),
                "recipient": header_map.get("To", ""),
                "date": header_map.get("Date", ""),
                "body": body_text,
                "content": content,
                "attachments": attachments,
                "snippet": message.get("snippet", ""),
            }
        except Exception as e:
            raise RuntimeError(f"failed email parsing: {e}")

    def _parse_payload(self, payload, message_id):
        """extract text body and attachment content"""
        try:
            text_parts = []
            attachments = []

            # get all parts (handles both single and multipart)
            parts = payload.get("parts", [payload])

            for part in parts:
                # multipart message
                if "parts" in part:
                    sub_body, _, sub_attach = self._parse_payload(part, message_id)
                    text_parts.append(sub_body)
                    attachments.extend(sub_attach)
                    continue

                mime_type = part.get("mimeType")
                body_data = part.get("body", {}).get("data")
                filename = part.get("filename")
                attachment_id = part.get("body", {}).get("attachmentId")

                if mime_type == "text/plain" and body_data:
                    decoded = base64.urlsafe_b64decode(body_data).decode(
                        "utf-8", errors="ignore"
                    )
                    text_parts.append(decoded)
                elif filename and attachment_id:
                    attachment_content = self._download_attachment(
                        attachment_id, filename, mime_type, message_id
                    )
                    if attachment_content:
                        attachments.append(
                            {
                                "filename": filename,
                                "mime_type": mime_type,
                                "content": attachment_content,
                            }
                        )

            body_text = "\n".join(text_parts).strip()

            # combine body and attachment content for embeddings
            content = body_text
            if attachments:
                attachment_texts = []
                for att in attachments:
                    if att["content"]:
                        attachment_texts.append(
                            f"Attachment '{att['filename']}': {att['content']}"
                        )
                if attachment_texts:
                    content += "\n\n" + "\n".join(attachment_texts)

            return body_text, content, attachments
        except Exception as e:
            raise RuntimeError(f"failed attachment parsing: {e}")

    def _download_attachment(self, attachment_id, filename, mime_type, message_id):
        """download and extract content from attachment"""
        try:
            if not self.service:
                self.auth()

            # download attachment data
            response = (
                self.service.users()
                .messages()
                .attachments()
                .get(userId="me", messageId=message_id, id=attachment_id)
                .execute()
            )

            data = base64.urlsafe_b64decode(response["data"])

            # extract content based on file type
            if mime_type == "application/pdf":
                return self._extract_pdf_content(data)
            elif mime_type.startswith("text/"):
                return data.decode("utf-8", errors="ignore")
            elif mime_type.startswith("image/"):
                return self._extract_image_content(data, filename)
            else:
                return f"[Binary file: {filename} - {mime_type}]"

        except Exception as e:
            print(f"Warning: failed to process attachment {filename}: {e}")
            return None

    def _extract_pdf_content(self, pdf_data):
        """extract text content from PDF"""
        try:
            pdf_file = io.BytesIO(pdf_data)
            pdf_reader = PdfReader(pdf_file)

            text_content = []
            for page in pdf_reader.pages:
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_content.append(page_text)
                except Exception:
                    continue

            return (
                "\n".join(text_content).strip()
                if text_content
                else "[PDF: No extractable text]"
            )

        except Exception as e:
            print(f"Warning: failed to extract PDF content: {e}")
            return "[PDF: Unable to extract text]"

    def _extract_image_content(self, image_data, filename):
        """extract text content from image using OCR"""
        try:
            image_file = io.BytesIO(image_data)
            image = Image.open(image_file)

            extracted_text = pytesseract.image_to_string(image)

            if extracted_text.strip():
                return f"[Image OCR from {filename}]: {extracted_text.strip()}"
            else:
                return f"[Image: {filename} - No text content found ]"

        except Exception as e:
            print(f"Warning: failed to extract text from image {filename}: {e}")
            return f"[Image: {filename} - OCR failed: {str(e)}]"


if __name__ == "__main__":
    g = Gmail()
    g.test()
    print(g.fetch(max_results=5))
