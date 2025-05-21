from fastapi import APIRouter, Response
from typing import Dict, Any, List, Optional

router = APIRouter()

@router.get("/robots.txt")
def get_robots_txt():
    """Generate and serve robots.txt file"""
    content = """User-agent: *
Allow: /

Sitemap: https://loufranktv.com/sitemap.xml

Disallow: /api/
"""
    return Response(content=content, media_type="text/plain")

@router.get("/sitemap.xml")
def get_sitemap_xml():
    """Generate and serve sitemap.xml file"""
    base_url = "https://loufranktv.com"
    today = "2025-03-10"
    
    # Define all site pages with their SEO properties
    pages = [
        # Main pages
        {"url": "/", "lastmod": today, "priority": "1.0", "changefreq": "weekly"},
        {"url": "/features", "lastmod": today, "priority": "0.8", "changefreq": "monthly"},
        {"url": "/pricing", "lastmod": today, "priority": "0.9", "changefreq": "monthly"},
        {"url": "/setup-guides", "lastmod": today, "priority": "0.7", "changefreq": "monthly"},
        {"url": "/testimonials", "lastmod": today, "priority": "0.6", "changefreq": "monthly"},
        {"url": "/faq", "lastmod": today, "priority": "0.7", "changefreq": "monthly"},
        {"url": "/contact", "lastmod": today, "priority": "0.6", "changefreq": "monthly"},
        {"url": "/about", "lastmod": today, "priority": "0.6", "changefreq": "monthly"},
        
        # Legal and policy pages
        {"url": "/privacy-policy", "lastmod": today, "priority": "0.5", "changefreq": "monthly"},
        {"url": "/terms-of-service", "lastmod": today, "priority": "0.5", "changefreq": "monthly"},
        {"url": "/refund-policy", "lastmod": today, "priority": "0.5", "changefreq": "monthly"},
        {"url": "/dmca", "lastmod": today, "priority": "0.4", "changefreq": "monthly"},
    ]
    
    # Generate XML sitemap
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml += '  <url>\n'
        xml += f'    <loc>{base_url}{page["url"]}</loc>\n'
        xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return Response(content=xml, media_type="application/xml")
