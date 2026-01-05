-- From reference:
-- <=> operator calculates the cosine distance between two vectors
-- Cosine distance is a measure of how different two vectors are, with 0 meaning they are identical and 1 meaning they are completely different
SELECT email_id, sender, recipient, subject, body, content, date, thread_id,
       1 - (embedding <=> %s::vector) as similarity
FROM email_vectors
ORDER BY embedding <=> %s::vector
LIMIT %s
