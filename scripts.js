// 文章列表数据，由Python生成
const posts = [
    { date: "2025-3-8", title: "2025-3-8" },
    { date: "2025-7-6", title: "2025-7-6" }
];

document.addEventListener('DOMContentLoaded', () => {
    console.log('scripts.js loaded');
    const currentDateSpan = document.getElementById('current-date');
    if (currentDateSpan) {
        const now = new Date();
        const dateStr = now.toISOString().split('T')[0];
        currentDateSpan.textContent = dateStr;
    } else {
        console.warn('Element with id "current-date" not found');
    }

    const postLists = document.querySelectorAll('.post-list');
    if (postLists.length > 0) {
        postLists.forEach(postList => {
            postList.innerHTML = '';
            posts.forEach(post => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = postList.classList.contains('sidebar-post-list') ? `${post.date}.html` : `posts/${post.date}.html`;
                a.textContent = post.title;
                li.appendChild(a);
                postList.appendChild(li);
            });
        });
    } else {
        console.log('No post-list elements found, likely on a post page without sidebar');
    }

    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');
    const closeBtn = document.querySelector('.modal-close');
    const prevBtn = document.querySelector('.modal-prev');
    const nextBtn = document.querySelector('.modal-next');
    const galleryImages = Array.from(document.querySelectorAll('.gallery img'));
    let currentImageIndex = 0;

    console.log(`Found ${galleryImages.length} images in .gallery`);
    if (modal && modalImg && closeBtn && prevBtn && nextBtn) {
        galleryImages.forEach((img, index) => {
            img.addEventListener('click', () => {
                console.log('Image clicked:', img.src);
                currentImageIndex = index;
                modalImg.src = img.src;
                modal.classList.add('show');
            });
        });

        prevBtn.addEventListener('click', () => {
            currentImageIndex = (currentImageIndex - 1 + galleryImages.length) % galleryImages.length;
            modalImg.src = galleryImages[currentImageIndex].src;
            console.log('Switched to previous image:', modalImg.src);
        });

        nextBtn.addEventListener('click', () => {
            currentImageIndex = (currentImageIndex + 1) % galleryImages.length;
            modalImg.src = galleryImages[currentImageIndex].src;
            console.log('Switched to next image:', modalImg.src);
        });

        closeBtn.addEventListener('click', () => {
            modal.classList.remove('show');
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
            }
        });
    } else {
        console.error('Modal elements not found:', {
            modal: !!modal,
            modalImg: !!modalImg,
            closeBtn: !!closeBtn,
            prevBtn: !!prevBtn,
            nextBtn: !!nextBtn
        });
    }
});
