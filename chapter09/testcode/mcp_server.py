from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP()

@mcp.tool()
def write_file(filename:str, content:str) -> str:
    """往文件文件中写入内容"""
    with open(f"D:/AITest/{filename}", "w", encoding="utf-8") as file:
        file.write(content)
    return f"文件{filename}写入成功"

@mcp.tool()
def get_weather(city:str) -> str:
    """查询某个城市或区县的天气"""
    amap_api_key = "46644f43e3a56ce81f6f3633c5994c67"
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={amap_api_key}&extensions=all"
    response = requests.get(url)
    return response.json()["forecasts"]

if __name__ == "__main__":
    # mcp.run(transport='stdio')  # 本地stdio调用
    # 远程sse方式调用
    mcp.settings.port = 8001  # 可自定义端口
    mcp.run(transport='sse')