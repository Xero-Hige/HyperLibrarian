Implement a class `Uploaders` with the methods:
    * `enqueue`: receives a string with a filename and enqueues it to upload
    * `flush`: upload all the enqueued files
    * `uploaded_files`: returns the number of files uploaded in the last flush
The upload works in a strict order of arrival, so the first enqueued files will be uploaded first. Each flush
can not upload more than 20b at the same time (20 chars). Consider implemented the class `Queue` with the methods:
`push`,`pop`,`head`,`empty`.