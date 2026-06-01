/**
 * 统一资源配置
 * 所有资源URL在此集中管理，便于后续替换
 */
const RESOURCE_CONFIG = {
    // 视频资源
    video: {
        demo: "//player.bilibili.com/player.html?bvid=BV号待替换"
    },

    // 下载资源
    download: {
        app: "蓝奏云链接待替换",
        aliDrive: "阿里云盘链接待替换"
    },

    // 图片资源
    images: {
        ocr: "SM.MS图片链接待替换",
        record: "SM.MS图片链接待替换",
        trigger: "SM.MS图片链接待替换",
        auth: "SM.MS图片链接待替换"
    }
};

// 导出配置
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { RESOURCE_CONFIG };
}