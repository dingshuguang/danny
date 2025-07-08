import os
from datetime import datetime

# HTML页面模板，包含侧边栏和底部按钮
page_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{date} 照片和故事</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="sidebar fade-in">
        <h3>日期导航</h3>
        <ul class="post-list sidebar-post-list">
            {post_list}
        </ul>
    </div>
    <header class="fade-in">
        <h1>{date}</h1>
        <p>当前日期：<span id="current-date">加载中...</span></p>
        <p><a href="../index.html" class="back-link">返回首页</a></p>
    </header>
    <section class="content fade-in">
        <h2>当天记录</h2>
        <p>这是{date}拍摄的照片。</p>
        <div class="gallery">
            {images}
        </div>
    </section>
    <div id="image-modal" class="modal">
        <span class="modal-close">×</span>
        <span class="modal-prev">←</span>
        <span class="modal-next">→</span>
        <img class="modal-content" id="modal-image">
    </div>
    <footer class="fade-in">
        <p><a href="../index.html" class="back-link">返回首页</a></p>
        <p>© 2025 我的个人博客. 保留所有权利。</p>
    </footer>
    <script src="../scripts.js"></script>
</body>
</html>'''

# 图片模板
image_template = '''<div class="image-container">
    <img src="../images/{date}/{filename}" alt="照片">
</div>'''

# 侧边栏文章列表模板
post_list_template = '''<li><a href="{href}">{title}</a></li>'''

# 确保posts文件夹存在
if not os.path.exists('posts'):
    os.makedirs('posts')

# 扫描images文件夹，生成页面
image_dir = 'images'
posts = []

for date_folder in os.listdir(image_dir):
    folder_path = os.path.join(image_dir, date_folder)
    if os.path.isdir(folder_path):
        # 验证日期格式（YYYY-MM-DD）
        try:
            datetime.strptime(date_folder, '%Y-%m-%d')
        except ValueError:
            continue

        # 获取图片文件（支持jpg、png）
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png'))]
        if images:
            # 生成图片HTML
            image_html = ''
            for img in images:
                image_html += image_template.format(date=date_folder, filename=img) + '\n'

            # 生成侧边栏文章列表
            post_list_html = ''
            for post in posts:
                post_list_html += post_list_template.format(href=f'{post["date"]}.html', title=post["title"]) + '\n'
            # 添加当前日期到列表
            post_list_html += post_list_template.format(href=f'{date_folder}.html', title=date_folder) + '\n'

            # 生成文章页面
            page_content = page_template.format(date=date_folder, images=image_html, post_list=post_list_html)
            with open(f'posts/{date_folder}.html', 'w', encoding='utf-8') as f:
                f.write(page_content)

            # 添加到文章列表（仅日期）
            posts.append({'date': date_folder, 'title': date_folder})

# 更新scripts.js
scripts_content = '''// 文章列表数据，由Python生成
const posts = [
    {posts}
];

document.addEventListener('DOMContentLoaded', () => {{
    console.log('scripts.js loaded');
    const currentDateSpan = document.getElementById('current-date');
    if (currentDateSpan) {{
        const now = new Date();
        const dateStr = now.toISOString().split('T')[0];
        currentDateSpan.textContent = dateStr;
    }} else {{
        console.warn('Element with id "current-date" not found');
    }}

    const postLists = document.querySelectorAll('.post-list');
    if (postLists.length > 0) {{
        postLists.forEach(postList => {{
            postList.innerHTML = '';
            posts.forEach(post => {{
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = postList.classList.contains('sidebar-post-list') ? `${{post.date}}.html` : `posts/${{post.date}}.html`;
                a.textContent = post.title;
                li.appendChild(a);
                postList.appendChild(li);
            }});
        }});
    }} else {{
        console.log('No post-list elements found, likely on a post page without sidebar');
    }}

    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');
    const closeBtn = document.querySelector('.modal-close');
    const prevBtn = document.querySelector('.modal-prev');
    const nextBtn = document.querySelector('.modal-next');
    const galleryImages = Array.from(document.querySelectorAll('.gallery img'));
    let currentImageIndex = 0;

    console.log(`Found ${{galleryImages.length}} images in .gallery`);
    if (modal && modalImg && closeBtn && prevBtn && nextBtn) {{
        galleryImages.forEach((img, index) => {{
            img.addEventListener('click', () => {{
                console.log('Image clicked:', img.src);
                currentImageIndex = index;
                modalImg.src = img.src;
                modal.classList.add('show');
            }});
        }});

        prevBtn.addEventListener('click', () => {{
            currentImageIndex = (currentImageIndex - 1 + galleryImages.length) % galleryImages.length;
            modalImg.src = galleryImages[currentImageIndex].src;
            console.log('Switched to previous image:', modalImg.src);
        }});

        nextBtn.addEventListener('click', () => {{
            currentImageIndex = (currentImageIndex + 1) % galleryImages.length;
            modalImg.src = galleryImages[currentImageIndex].src;
            console.log('Switched to next image:', modalImg.src);
        }});

        closeBtn.addEventListener('click', () => {{
            modal.classList.remove('show');
        }});

        modal.addEventListener('click', (e) => {{
            if (e.target === modal) {{
                modal.classList.remove('show');
            }}
        }});
    }} else {{
        console.error('Modal elements not found:', {{
            modal: !!modal,
            modalImg: !!modalImg,
            closeBtn: !!closeBtn,
            prevBtn: !!prevBtn,
            nextBtn: !!nextBtn
        }});
    }}
}});
'''

# 将posts列表格式化为JavaScript数组
posts_str = ',\n    '.join([f'{{ date: "{p["date"]}", title: "{p["title"]}" }}' for p in posts])
with open('scripts.js', 'w', encoding='utf-8') as f:
    f.write(scripts_content.format(posts=posts_str))

print(f'已生成 {len(posts)} 个文章页面')