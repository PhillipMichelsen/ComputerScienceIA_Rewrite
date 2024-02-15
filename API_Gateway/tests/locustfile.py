from locust import HttpUser, task


class FileServiceTest(HttpUser):
    @task
    def presigned_upload_url_test(self):
        self.client.get("/get_presigned_upload_url?file_name=test.pdf")
