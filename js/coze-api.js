/**
 * Coze KV API 封装
 * 用于公告数据的存储和读取
 */
const CozeAPI = {
    // 配置 - 使用时需要填入你的 Token
    CONFIG: {
        APP_ID: "7601886661592596489",
        WORKFLOW_ID_GET: "7601964817507500051",
        WORKFLOW_ID_SET: "7601964680655454249",
        BASE_URL: "https://api.coze.cn/v1/workflow/run",
        TOKEN: ""  // 在使用前设置 Token
    },

    /**
     * 设置 API Token
     */
    setToken(token) {
        this.CONFIG.TOKEN = token;
    },

    /**
     * 运行工作流
     */
    async runWorkflow(workflowId, parameters) {
        const payload = {
            workflow_id: workflowId,
            app_id: this.CONFIG.APP_ID,
            parameters: parameters
        };

        try {
            const response = await fetch(this.CONFIG.BASE_URL, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.CONFIG.TOKEN}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Workflow execution error:', error);
            return null;
        }
    },

    /**
     * 获取 KV 值
     */
    async get(key) {
        const result = await this.runWorkflow(this.CONFIG.WORKFLOW_ID_GET, { kv_key: key });
        
        if (!result) return null;

        try {
            const data = JSON.parse(result.data || '{}');
            let value = data.kv_value;
            
            // 尝试解析 JSON
            if (typeof value === 'string') {
                try {
                    return JSON.parse(value);
                } catch {
                    return value;
                }
            }
            return value;
        } catch (e) {
            console.error('Parse error:', e);
            return null;
        }
    },

    /**
     * 设置 KV 值
     */
    async set(key, value) {
        const valueStr = typeof value === 'object' ? JSON.stringify(value, null, 2) : value;
        const result = await this.runWorkflow(this.CONFIG.WORKFLOW_ID_SET, {
            kv_key: key,
            kv_value: valueStr
        });

        if (!result) return false;

        try {
            const data = JSON.parse(result.data || '{}');
            return data.success === true;
        } catch {
            return false;
        }
    }
};

/**
 * 公告管理模块
 */
const NoticeManager = {
    STORAGE_KEY: "yanyun_notices",

    /**
     * 获取所有公告
     */
    async getNotices() {
        const data = await CozeAPI.get(this.STORAGE_KEY);
        if (data && Array.isArray(data.notices)) {
            return data.notices;
        }
        return [];
    },

    /**
     * 保存所有公告
     */
    async saveNotices(notices) {
        return await CozeAPI.set(this.STORAGE_KEY, { notices: notices });
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

// 导出（支持 ES Module 和全局变量）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CozeAPI, NoticeManager };
}
