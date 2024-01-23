from httpx import AsyncClient


async def test_get_metrics(client: AsyncClient):
    resp = await client.get('/metrics')
    assert resp.status_code == 200
    up_string = 'up{app="pics_dataset"} 1.0'
    assert up_string in resp.text, resp.text
