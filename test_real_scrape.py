#!/usr/bin/env python3
"""
真实测试 AWS-008 番号刮削流程
"""
import asyncio
import sys
from pathlib import Path
from mdcx.number import get_file_number, is_uncensored, is_suren
from mdcx.config.models import Config, Website
from mdcx.models.types import CrawlerInput, CrawlTask
from mdcx.core.file_crawler import FileScraper
from mdcx.crawler import CrawlerProvider
from mdcx.web_async import AsyncWebClient
from mdcx.config.enums import Language
from mdcx.models.enums import FileMode
import os
import json
from datetime import datetime


async def real_test_scrape_aws008():
    print("=" * 80)
    print("🚀 AWS-008 真实刮削测试")
    print("=" * 80)
    
    # 创建输出目录
    output_dir = Path("/workspace/test_output")
    output_dir.mkdir(exist_ok=True)
    print(f"\n输出目录: {output_dir}")
    
    # Step 1: 番号识别
    print("\n【Step 1】番号识别")
    print("-" * 80)
    test_number = "AWS-008"
    file_number = get_file_number(test_number, [])
    print(f"输入文件名: {test_number}")
    print(f"提取番号: {file_number}")
    
    # Step 2: 判断番号类型
    print("\n【Step 2】番号类型判断")
    print("-" * 80)
    uncensored = is_uncensored(test_number)
    suren_flag = is_suren(test_number)
    print(f"是否无码流出: {uncensored}")
    print(f"是否素人番号: {suren_flag}")
    
    # Step 3: 加载配置
    print("\n【Step 3】加载配置")
    print("-" * 80)
    config = Config()
    
    # 确保输出目录
    config.media_path = str(output_dir)
    config.success_output_folder = "success"
    config.failed_output_folder = "failed"
    
    print(f"媒体路径: {config.media_path}")
    
    # Step 4: 初始化客户端和爬虫提供者
    print("\n【Step 4】初始化客户端和爬虫提供者")
    print("-" * 80)
    client = AsyncWebClient(timeout=60.0, retry=2)
    crawler_provider = CrawlerProvider(config, client)
    print("✅ 客户端和爬虫提供者已创建")
    
    # Step 5: 创建文件扫描器
    print("\n【Step 5】创建文件扫描器")
    print("-" * 80)
    file_scraper = FileScraper(config, crawler_provider)
    print("✅ 文件扫描器已创建")
    
    # Step 6: 准备刮削任务
    print("\n【Step 6】准备刮削任务")
    print("-" * 80)
    crawl_task = CrawlTask.empty()
    crawl_task.number = file_number
    crawl_task.appoint_number = ""
    crawl_task.appoint_url = ""
    crawl_task.mosaic = ""
    crawl_task.short_number = ""
    crawl_task.leak = ""
    crawl_task.destroyed = ""
    crawl_task.wuma = ""
    crawl_task.youma = ""
    crawl_task.c_word = ""
    crawl_task.cd_part = ""
    crawl_task.has_sub = False
    crawl_task.website_name = ""
    crawl_task.file_path = None
    print(f"✅ 任务准备完成: {file_number}")
    
    # Step 7: 真实执行刮削
    print("\n【Step 7】执行真实刮削")
    print("-" * 80)
    print("⚠️  注意: 此步骤可能需要网络连接")
    print("⚠️  如果网络请求可能会失败，我们会尝试所有网站")
    
    result = None
    try:
        # 先尝试用单个网站测试 (javbus)
        print(f"\n1️⃣  首先尝试从 javbus 刮取...")
        try:
            print("-" * 80)
            crawl_task.website_name = "javbus"
            result_javbus = await file_scraper.run(crawl_task, FileMode.Again)
            if result_javbus:
                print(f"✅ 从 javbus 成功获取数据!")
                result = result_javbus
                await save_result(output_dir, "javbus", result)
        except Exception as e:
            print(f"❌ javbus 失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 如果 javbus 失败，尝试其他网站
        if not result:
            print(f"\n2️⃣  尝试其他素人网站组...")
            try:
                crawl_task.website_name = ""
                result = await file_scraper.run(crawl_task, FileMode.Single)
                if result:
                    print(f"✅ 成功获取数据!")
                    await save_result(output_dir, "all_sites", result)
            except Exception as e:
                print(f"❌ 失败: {e}")
                import traceback
                traceback.print_exc()
        
        # 如果没有网络请求，保存演示数据
        if not result:
            print(f"\n📊 生成演示数据...")
            result = generate_demo_data(file_number)
            await save_result(output_dir, "demo", result, is_demo=True)
    
    except Exception as e:
        print(f"\n❌ 刮削过程出错: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n📊 生成演示数据...")
        result = generate_demo_data(file_number)
        await save_result(output_dir, "demo", result, is_demo=True)
    
    finally:
        # Step 8: 关闭资源
        print("\n【Step 8】清理资源")
        print("-" * 80)
        await crawler_provider.close()
    
    print("\n" + "=" * 80)
    print("🎉 刮削流程完成!")
    print("=" * 80)
    
    # 列出产出物
    print(f"\n📁 产出物列表:")
    for item in output_dir.glob("**/*"):
        if item.is_file():
            size = item.stat().st_size
            print(f"  • {item.relative_to(output_dir)} ({size:,} bytes)")
    
    print(f"\n✅ 所有文件已保存到: {output_dir}")


def generate_demo_data(number):
    """生成演示数据，用于网络请求失败时"""
    from mdcx.models.types import CrawlersResult
    
    result = CrawlersResult.empty()
    result.number = number
    result.title = f"{number} - Amazon Original Series Demo"
    result.originaltitle = f"{number} - Amazon Original Series"
    result.outline = "这是演示数据的简介。由于网络限制，我们生成了这些演示内容。\n实际使用真实网络请求时会替换为真实内容。"
    result.release = "2024-01-15"
    result.year = "2024"
    result.runtime = 120
    result.score = "8.5"
    result.studio = "Amazon Studios"
    result.publisher = "Amazon"
    result.series = "AWS Series"
    result.actors = ["Demo Actress 1", "Demo Actress 2"]
    result.tags = ["Demo", "Amazon", "AWS"]
    result.poster = "https://via.placeholder.com/400x600/0066cc/ffffff?text=AWS-008+Poster"
    result.thumb = "https://via.placeholder.com/200x300/009933/ffffff?text=Thumb"
    result.mosaic = "有码"
    result.field_log = "演示数据字段来源"
    result.site_log = "演示数据网站日志"
    return result


async def save_result(output_dir, source, result, is_demo=False):
    """保存结果到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_name = f"{source}_{timestamp}"
    result_dir = output_dir / dir_name
    result_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 保存结果到: {result_dir}")
    
    # 1. 保存 JSON 数据
    json_data = {
        "number": result.number,
        "title": result.title,
        "originaltitle": result.originaltitle,
        "outline": result.outline,
        "release": result.release,
        "year": result.year,
        "runtime": result.runtime,
        "score": result.score,
        "studio": result.studio,
        "publisher": result.publisher,
        "series": result.series,
        "actors": result.actors,
        "tags": result.tags,
        "poster": result.poster,
        "thumb": result.thumb,
        "mosaic": result.mosaic,
        "is_demo": is_demo,
        "saved_at": datetime.now().isoformat(),
    }
    
    json_file = result_dir / f"{result.number}_data.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ JSON 数据已保存: {json_file.name}")
    
    # 2. 保存 NFO 文件
    nfo_content = generate_nfo(result)
    nfo_file = result_dir / f"{result.number}.nfo"
    with open(nfo_file, "w", encoding="utf-8") as f:
        f.write(nfo_content)
    print(f"  ✅ NFO 文件已保存: {nfo_file.name}")
    
    # 3. 保存演示图片（如果有 URL 可用）
    if result.poster:
        try:
            poster_file = result_dir / f"{result.number}_poster.jpg"
            print(f"  🖼️  尝试下载海报: {result.poster}")
            # 使用 httpx 下载图片
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(result.poster, follow_redirects=True)
                if resp.status_code == 200:
                    with open(poster_file, "wb") as f:
                        f.write(resp.content)
                    print(f"    ✅ 海报已保存: {poster_file.name} ({len(resp.content)} bytes")
        except Exception as e:
            print(f"    ⚠️  海报下载: {e}，但已尝试保存占位符")
            # 生成占位符图片内容
            placeholder = create_placeholder_image(result.number)
            with open(poster_file, "wb") as f:
                f.write(placeholder)
    
    if result.thumb:
        try:
            thumb_file = result_dir / f"{result.number}_thumb.jpg"
            print(f"  🖼️  尝试下载缩略图: {result.thumb}")
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(result.thumb, follow_redirects=True)
                if resp.status_code == 200:
                    with open(thumb_file, "wb") as f:
                        f.write(resp.content)
                    print(f"    ✅ 缩略图已保存: {thumb_file.name} ({len(resp.content)} bytes")
        except Exception as e:
            print(f"    ⚠️  缩略图下载: {e}")
    
    # 4. 保存字段日志
    log_file = result_dir / "scrape_log.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write(f"刮削日志 - {result.number}\n")
        f.write("="*80 + "\n\n")
        f.write(f"来源: {source}\n")
        f.write(f"演示数据: {is_demo}\n")
        f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("-"*80 + "\n")
        f.write("字段日志:\n")
        f.write(result.field_log + "\n\n")
        f.write("-"*80 + "\n")
        f.write("网站日志:\n")
        f.write(result.site_log + "\n")
    print(f"  ✅ 日志已保存: {log_file.name}")
    
    print(f"\n📂 保存位置: {result_dir}")
    return result_dir


def generate_nfo(result):
    """生成 NFO 元数据文件"""
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    nfo = f"""<?xml version="1.0" encoding="UTF-8"?>
<movie>
  <title>{result.title}</title>
  <originaltitle>{result.originaltitle}</originaltitle>
  <sorttitle>{result.number}</sorttitle>
  <set>
    <name>{result.series}</name>
  </set>
  <rating>{result.score}</rating>
  <year>{result.year}</year>
  <top250>0</top250>
  <votes>0</votes>
  <outline>{result.outline}</outline>
  <plot>{result.outline}</plot>
  <tagline></tagline>
  <runtime>{result.runtime}</runtime>
  <thumb>{result.poster}</thumb>
  <fanart>{result.thumb}</fanart>
  <mpaa>XXX</mpaa>
  <playcount>0</playcount>
  <lastplayed></lastplayed>
  <fileinfo>
    <streamdetails>
    </streamdetails>
  </fileinfo>
  <id>{result.number}</id>
  <genre>Adult</genre>
  <studio>{result.studio}</studio>
  <premiered>{result.release}</premiered>
  <year>{result.year}</year>
  <rating>{result.score}</rating>
  <votes>1</votes>
  <outline>{result.outline}</outline>
  <plot>{result.outline}</plot>
  <tagline>{result.title}</tagline>
  <runtime>{result.runtime}</runtime>
  <mpaa>Rated XXX</mpaa>
  <genre>Adult</genre>
  <genre>AWS</genre>
  <genre>Amazon</genre>
  <country>Japan</country>
  <id>{result.number}</id>
</movie>
"""
    
    # 添加演员
    for actor in result.actors:
        nfo += f"""  <actor>
    <name>{actor}</name>
    <role></role>
    <thumb></thumb>
  </actor>
"""
    
    nfo += "</movie>"
    return nfo


def create_placeholder_image(number):
    """创建简单的占位符图片"""
    # 使用 Pillow 创建简单的占位符图片
    from PIL import Image, ImageDraw, ImageFont
    import io
    
    img = Image.new('RGB', (400, 600), color='#1a73e8')
    d = ImageDraw.Draw(img)
    
    # 绘制文本
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        # 如果没有字体，使用默认
        font = ImageFont.load_default()
    
    # 居中绘制文本
    text = f"{number}"
    # 使用 textbbox 获取文本大小
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (400 - text_width) / 2
    y = (600 - text_height) / 2 - 50
    
    d.text((x, y), text, fill='white', font=font)
    
    # 绘制副标题
    subtitle = "Demo Image"
    try:
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        subtitle_font = ImageFont.load_default()
    
    bbox2 = d.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_width = bbox2[2] - bbox2[0]
    sub_height = bbox2[3] - bbox2[1]
    
    sub_x = (400 - sub_width) / 2
    sub_y = y + text_height + 30
    
    d.text((sub_x, sub_y), subtitle, fill='white', font=subtitle_font)
    
    # 保存到内存
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes.read()


if __name__ == "__main__":
    asyncio.run(real_test_scrape_aws008())
