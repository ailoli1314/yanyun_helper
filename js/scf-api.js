/**
 * SCF KV API 封装
 * 基于腾讯云云函数 + COS 的键值存储
 * 替代原 Coze KV
 */
const SCF_API = {
    BASE_URL: "https://1258077315-i5iw5btpg1.ap-guangzhou.tencentscf.com",
    NOTICE_KEY: "notice:yanyun_notices",
    CONFIG_KEY: "resource_config",
    apiKey: "",

    /**
     * 设置 API Key（写入操作需要）
     */
    setApiKey(key) {
        this.apiKey = key;
    },

    /**
     * 读取 KV 值（无需鉴权）
     */
    async get(key) {
        try {
            const resp = await fetch(`${this.BASE_URL}/kv?key=${encodeURIComponent(key)}`);
            if (!resp.ok) return null;
            const text = await resp.text();
            if (!text || text.trim() === 'null') return null;
            try { return JSON.parse(text); } catch { return text; }
        } catch (e) {
            console.error('SCF_API.get error:', e);
            return null;
        }
    },

    /**
     * 写入 KV 值（需要 API Key 鉴权）
     */
    async set(key, value) {
        if (!this.apiKey) {
            console.error('SCF_API.set: 未设置 API Key');
            return false;
        }
        const body = typeof value === 'string' ? value : JSON.stringify(value);
        try {
            const resp = await fetch(`${this.BASE_URL}/kv`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-API-Key': this.apiKey },
                body: JSON.stringify({ key, value: body })
            });
            if (resp.status === 403) {
                console.error('SCF_API.set: API Key 无效');
                return false;
            }
            const result = await resp.json();
            return result.success === true;
        } catch (e) {
            console.error('SCF_API.set error:', e);
            return false;
        }
    },

    /**
     * 验证 API Key 是否正确
     */
    async verifyApiKey(key) {
        try {
            const resp = await fetch(`${this.BASE_URL}/kv/verify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-API-Key': key },
                body: JSON.stringify({})
            });
            const result = await resp.json();
            return result.valid === true;
        } catch (e) {
            console.error('SCF_API.verifyApiKey error:', e);
            return false;
        }
    }
};

/**
 * 公告管理模块
 */
const NoticeManager = {
    STORAGE_KEY: SCF_API.NOTICE_KEY,

    /**
     * 获取所有公告
     */
    async getNotices() {
        const data = await SCF_API.get(this.STORAGE_KEY);
        if (data && Array.isArray(data.notices)) {
            return data.notices;
        }
        return [];
    },

    /**
     * 保存所有公告（需要 API Key）
     */
    async saveNotices(notices) {
        return await SCF_API.set(this.STORAGE_KEY, { notices: notices });
    },

    /**
     * 添加公告
     */
    async addNotice(notice) {
        const notices = await this.getNotices();
        notice.id = Date.now().toString();
        notice.date = new Date().toISOString().split('T')[0];
        notices.unshift(notice);
        return await this.saveNotices(notices);
    },

    /**
     * 删除公告
     */
    async deleteNotice(id) {
        const notices = await this.getNotices();
        const filtered = notices.filter(n => n.id !== id);
        return await this.saveNotices(filtered);
    },

    /**
     * 更新公告
     */
    async updateNotice(id, updates) {
        const notices = await this.getNotices();
        const index = notices.findIndex(n => n.id === id);
        if (index !== -1) {
            notices[index] = { ...notices[index], ...updates };
            return await this.saveNotices(notices);
        }
        return false;
    },

    /**
     * 获取类型标签文本
     */
    getTypeLabel(type) {
        const labels = {
            'hot': '热门',
            'update': '更新',
            'discount': '优惠',
            'notice': '公告',
            'tutorial': '教程'
        };
        return labels[type] || '公告';
    },

    /**
     * 获取类型对应的 emoji
     */
    getTypeEmoji(type) {
        const emojis = {
            'hot': '🔥',
            'update': '🔧',
            'discount': '💰',
            'notice': '📢',
            'tutorial': '📚'
        };
        return emojis[type] || '📢';
    }
};

/**
 * 云端资源配置模块
 * 替代本地 config.js，通过 KV 存储读写配置
 */
const CloudConfig = {
    /** 缓存的配置数据 */
    _cache: null,

    /** 默认配置（云端无数据时的兜底） */
    DEFAULT: {
        video: { demo: "" },
        download: { baiduPan: "", aliDrive: "", lanzou: "" },
        images: { ocr: "", record: "", trigger: "", auth: "" }
    },

    /**
     * 从云端获取配置（公开读取，无需鉴权）
     * 返回完整配置对象，失败则返回默认配置
     */
    async get() {
        try {
            const data = await SCF_API.get(SCF_API.CONFIG_KEY);
            if (data && typeof data === 'object' && !data.error) {
                this._cache = data;
                return data;
            }
        } catch (e) {
            console.error('CloudConfig.get error:', e);
        }
        return this._cache || { ...this.DEFAULT };
    },

    /**
     * 保存配置到云端（需要 API Key 鉴权）
     */
    async save(config) {
        const success = await SCF_API.set(SCF_API.CONFIG_KEY, config);
        if (success) {
            this._cache = config;
        }
        return success;
    }
};

// 导出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SCF_API, NoticeManager, CloudConfig };
}
