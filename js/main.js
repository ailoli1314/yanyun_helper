// 燕云脚本官网交互逻辑
document.addEventListener('DOMContentLoaded', function() {
    // 导航栏滚动效果
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 100) {
            navbar.style.background = 'rgba(30, 30, 46, 0.95)';
        } else {
            navbar.style.background = 'rgba(30, 30, 46, 0.9)';
        }
        lastScroll = currentScroll;
    });

    // 平滑滚动（排除外部链接和下载按钮）
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            // 如果 href 已被更新为外部链接，不拦截
            const href = this.getAttribute('href');
            if (href && href !== '#' && !href.startsWith('#')) return;
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // 下载按钮点击反馈
    const downloadBtns = document.querySelectorAll('#navDownload, #heroDownload, #footerDownload');
    downloadBtns.forEach(btn => {
        if (btn) {
            btn.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (!href || href === '#') {
                    e.preventDefault();
                    console.log('下载链接尚未配置');
                }
            });
        }
    });

    // 订阅表单提交
    const subscribeForm = document.querySelector('.subscribe-form');
    if (subscribeForm) {
        subscribeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value;
            if (email) {
                alert('感谢订阅！我们会不定期发送最新公告到您的邮箱。');
                emailInput.value = '';
            }
        });
    }

    // 卡片悬停动画增强
    const cards = document.querySelectorAll('.feature-card, .notice-card, .scene-card, .step-item');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });

    // 公告卡片点击
    const noticeLinks = document.querySelectorAll('.notice-link');
    noticeLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            alert('详情页面开发中，敬请期待！');
        });
    });

    // 页面加载动画
    const body = document.body;
    body.style.opacity = '0';
    setTimeout(() => {
        body.style.transition = 'opacity 0.5s ease';
        body.style.opacity = '1';
    }, 100);

    // 滚动显示动画
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .notice-card, .scene-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});
