import httpx
import asyncio
from fastapi import HTTPException


class BanditModelClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(300.0))

    async def start(self, data: dict):
        response = await self.client.post(
            f"{self.base_url}/pipeline/make-fasta", json=data
        )
        return response.json()

    async def update(self, data: dict):
        response = await self.client.post(
            "{}/pipeline/feedback".format(self.base_url), json=data
        )
        return response.json()

    async def get_training_status(self, training_id: str):
        response = await self.client.get(f"{self.base_url}/status/{training_id}")
        return response.json()

    async def get_model_metrics(self, model_id: str):
        response = await self.client.get(f"{self.base_url}/metrics/{model_id}")
        return response.json()

    async def stop_training(self, training_id: str):
        response = await self.client.post(f"{self.base_url}/stop/{training_id}")
        return response.json()

    async def close(self):
        await self.client.aclose()


class FoldModelClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(2700.0))

    async def start(self, data: dict):
        response = await self.client.post(f"{self.base_url}/fold/start", json=data)
        return response.json()

    async def start_multi(self, data: dict):
        response = await self.client.post(
            f"{self.base_url}/fold/start-multi", json=data
        )
        return response.json()

    async def update(self, data: dict):
        response = await self.client.post(
            "{}/pipeline/update".format(self.base_url), json=data
        )
        return response.json()

    async def get_training_status(self, training_id: str):
        response = await self.client.get(f"{self.base_url}/status/{training_id}")
        return response.json()

    async def get_model_metrics(self, model_id: str):
        response = await self.client.get(f"{self.base_url}/metrics/{model_id}")
        return response.json()

    async def stop_training(self, training_id: str):
        response = await self.client.post(f"{self.base_url}/stop/{training_id}")
        return response.json()

    async def close(self):
        await self.client.aclose()


class DockModelClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(1800.0))

    async def start(self, data: dict):
        try:
            response = await self.client.post(f"{self.base_url}/dock/start", json=data)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail=f"Error: {response.text}"
                )

            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=response.status_code, detail=f"HTTP error occurred: {e}"
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error occurred: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    async def upload(self, data: dict, files: dict):
        response = await self.client.post(
            "{}/dock/pdb/save".format(self.base_url), data=data, files=files
        )
        return response.json()

    async def update(self, data: dict):
        response = await self.client.post(
            "{}/pipeline/update".format(self.base_url), json=data
        )
        return response.json()

    async def get_training_status(self, training_id: str):
        response = await self.client.get(f"{self.base_url}/status/{training_id}")
        return response.json()

    async def get_model_metrics(self, model_id: str):
        response = await self.client.get(f"{self.base_url}/metrics/{model_id}")
        return response.json()

    async def stop_training(self, training_id: str):
        response = await self.client.post(f"{self.base_url}/stop/{training_id}")
        return response.json()

    async def close(self):
        await self.client.aclose()