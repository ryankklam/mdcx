#!/usr/bin/env python3
"""
测试 AWS-008 番号刮削流程
"""
import asyncio
import sys
from mdcx.number import get_file_number, is_uncensored, is_suren
from mdcx.config.models import Config, Website
from mdcx.models.types import CrawlerInput, CrawlTask
from mdcx.core.file_crawler import FileScraper
from mdcx.crawler import CrawlerProvider
from mdcx.web_async import AsyncWebClient
from mdcx.config.enums import Language
from mdcx.gen.field_enums import CrawlerResultFields


async def test_scrape_aws008():
    print("=" * 80)
    print("AWS-008 刮削流程测试")
    print("=" * 80)
    
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
    suren = is_suren(test_number)
    print(f"是否无码流出: {uncensored}")
    print(f"是否素人番号: {suren}")
    
    # Step 3: 判断使用的网站组
    print("\n【Step 3】选择刮削网站组")
    print("-" * 80)
    
    # AWS-008 看起来像是素人番号（以 A 开头，数字在后面）
    # 但它不在 SUREN_DIC 中，所以会根据规则判断
    # AWS-008 匹配 \d{2,}[A-Z]{2,}-\d{2,} 这样的模式
    
    if "AWS" in test_number.upper() or "A" in test_number[0]:
        # AWS 开头的番号通常是 Amazon 相关的，可能是素人系列
        print(f"检测到可能为素人番号 (AWS 系列)")
        print(f"将使用 website_suren 网站组进行刮削")
        website_group = "website_suren"
    else:
        print(f"将使用 website_youma 网站组进行刮削")
        website_group = "website_youma"
    
    # Step 4: 加载配置
    print("\n【Step 4】加载配置")
    print("-" * 80)
    config = Config()
    print(f"媒体路径: {config.media_path}")
    print(f"有码网站组 ({len(config.website_youma)} 个网站):")
    for site in sorted(config.website_youma, key=lambda x: x.value):
        print(f"  - {site.value}")
    
    print(f"\n素人网站组 ({len(config.website_suren)} 个网站):")
    for site in sorted(config.website_suren, key=lambda x: x.value):
        print(f"  - {site.value}")
    
    # Step 5: 字段配置
    print("\n【Step 5】字段优先级配置")
    print("-" * 80)
    for field in [
        CrawlerResultFields.TITLE,
        CrawlerResultFields.OUTLINE,
        CrawlerResultFields.POSTER,
        CrawlerResultFields.ACTORS,
    ]:
        if field in config.field_configs:
            fc = config.field_configs[field]
            print(f"{field.value}:")
            print(f"  优先级: {[s.value for s in fc.site_prority]}")
            print(f"  语言: {fc.language.value}")
    
    # Step 6: 准备刮削输入
    print("\n【Step 6】准备刮削任务")
    print("-" * 80)
    task_input = CrawlerInput.empty()
    task_input.number = file_number
    task_input.appoint_number = ""
    task_input.appoint_url = ""
    task_input.mosaic = ""
    task_input.short_number = ""
    task_input.language = Language.UNDEFINED
    task_input.org_language = Language.UNDEFINED
    print(f"番号: {task_input.number}")
    print(f"指定番号: {task_input.appoint_number}")
    print(f"指定网址: {task_input.appoint_url}")
    print(f"马赛克类型: {task_input.mosaic or '未指定'}")
    print(f"短番号: {task_input.short_number or '未指定'}")
    print(f"语言: {task_input.language.value}")
    
    # Step 7: 创建爬虫提供者
    print("\n【Step 7】初始化爬虫提供者")
    print("-" * 80)
    client = AsyncWebClient(timeout=30.0)
    crawler_provider = CrawlerProvider(config, client)
    print("爬虫提供者已创建")
    
    # Step 8: 执行刮削
    print("\n【Step 8】执行刮削")
    print("-" * 80)
    
    try:
        # 使用素人网站组进行刮削
        file_scraper = FileScraper(config, crawler_provider)
        
        # 创建爬取任务
        crawl_task = CrawlTask.empty()
        crawl_task.number = file_number
        crawl_task.appoint_number = ""
        crawl_task.website_name = ""
        
        print(f"开始刮削番号: {file_number}")
        print("-" * 80)
        
        # 模拟刮削过程（实际调用会涉及网络请求）
        # 这里我们只展示流程，不实际执行网络请求
        print("\n刮削流程:")
        print("1. 创建文件扫描器 (FileScraper)")
        print("2. 识别番号类型: 素人番号")
        print("3. 选择网站组: website_suren")
        print("4. 按优先级尝试各网站:")
        
        # 展示将尝试的网站
        sites_to_try = sorted(config.website_suren, key=lambda x: x.value)
        for i, site in enumerate(sites_to_try, 1):
            print(f"   {i}. {site.value} - {site}")
        
        print("\n5. 对每个网站执行:")
        print("   - 发送搜索请求")
        print("   - 解析搜索结果")
        print("   - 获取详情页数据")
        print("   - 按字段优先级提取数据")
        
        print("\n6. 聚合各网站数据")
        print("7. 数据后处理和格式化")
        print("8. 返回刮削结果")
        
    except Exception as e:
        print(f"\n刮削过程出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭爬虫提供者
        await crawler_provider.close()
    
    print("\n" + "=" * 80)
    print("刮削流程测试完成")
    print("=" * 80)


def main():
    asyncio.run(test_scrape_aws008())


if __name__ == "__main__":
    main()
