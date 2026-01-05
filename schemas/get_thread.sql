SELECT email_id, sender, recipient, subject, body, content, date, thread_id, 1.0 as similarity
FROM email_vectors 
WHERE thread_id = %s::text
ORDER BY date ASC