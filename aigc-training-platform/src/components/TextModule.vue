<template>
  <div class="text-module">
    <div class="module-header">
      <div class="header-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
        </svg>
      </div>
      <div class="header-text">
        <h2>文本生成</h2>
        <p>基于AI的智能文本处理工具</p>
      </div>
    </div>

    <div class="tabs-container">
      <button 
        v-for="tab in tabs" 
        :key="tab.key"
        :class="['tab-btn', { active: activeTab === tab.key }]"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <div class="content-area">
      <div class="input-section">
        <label class="input-label">{{ currentTabConfig.label }}</label>
        <textarea
          v-model="inputText"
          :placeholder="currentTabConfig.placeholder"
          :maxlength="500"
          class="text-input"
          rows="5"
        ></textarea>
        <span class="char-count">{{ inputText.length }}/500</span>
      </div>

      <button 
        class="generate-btn"
        :disabled="!inputText.trim() || isLoading"
        :class="{ loading: isLoading }"
        @click="handleGenerate"
      >
        <span>{{ isLoading ? '生成中...' : currentTabConfig.buttonText }}</span>
      </button>

      <div v-if="resultData" class="result-section">
        <div class="result-header">
          <span class="result-title">生成结果</span>
          <span class="response-time">响应时间: {{ responseTime }}ms</span>
        </div>
        <div class="result-content">
          <p>{{ resultData.content }}</p>
        </div>
        <div class="result-actions">
          <button class="action-btn" @click="copyResult">复制结果</button>
          <button class="action-btn" @click="downloadResult">下载</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const tabs = [
  { key: 'generate', label: '文本生成' },
  { key: 'polish', label: '文本润色' },
  { key: 'rewrite', label: '文本改写' },
  { key: 'summarize', label: '文本摘要' },
  { key: 'optimize', label: '提示词优化' }
]

const activeTab = ref('generate')
const inputText = ref('')
const isLoading = ref(false)
const resultData = ref(null)
const responseTime = ref(0)

const currentTabConfig = computed(() => {
  const configs = {
    generate: { label: '输入主题或关键词', placeholder: '请输入您想要生成的文本主题...', buttonText: '生成文本' },
    polish: { label: '输入需要润色的文本', placeholder: '请输入需要润色的文本内容...', buttonText: '润色文本' },
    rewrite: { label: '输入需要改写的文本', placeholder: '请输入需要改写的文本内容...', buttonText: '改写文本' },
    summarize: { label: '输入需要摘要的文本', placeholder: '请输入需要摘要的文本内容...', buttonText: '生成摘要' },
    optimize: { label: '输入需要优化的提示词', placeholder: '请输入需要优化的提示词...', buttonText: '优化提示词' }
  }
  return configs[activeTab.value] || configs.generate
})

const handleGenerate = async () => {
  if (!inputText.value.trim()) return
  
  isLoading.value = true
  resultData.value = null
  const startTime = Date.now()
  
  try {
    const taskTypeMap = {
      generate: 'generate',
      polish: 'polish',
      rewrite: 'rewrite',
      summarize: 'summary',
      optimize: 'optimize'
    }

    const response = await fetch('http://localhost:8000/api/text/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        prompt: inputText.value,
        task_type: taskTypeMap[activeTab.value] || 'generate'
      })
    })

    const data = await response.json()
    responseTime.value = Date.now() - startTime
    
    if (data && data.content) {
      resultData.value = data
      
      const history = JSON.parse(localStorage.getItem('creationHistory') || '[]')
      history.unshift({
        id: Date.now(),
        type: 'text',
        title: inputText.value.substring(0, 30) + (inputText.value.length > 30 ? '...' : ''),
        content: data.content,
        time: getTimeAgo(),
        createdAt: new Date().toISOString()
      })
      localStorage.setItem('creationHistory', JSON.stringify(history.slice(0, 50)))
    } else {
      resultData.value = { content: '生成失败，请重试' }
    }
  } catch (error) {
    console.error('API调用失败:', error)
    responseTime.value = Date.now() - startTime
    resultData.value = { content: '网络错误，请检查后端服务是否正常运行' }
  } finally {
    isLoading.value = false
  }
}

const copyResult = async () => {
  try {
    await navigator.clipboard.writeText(resultData.value?.content || '')
    alert('已复制到剪贴板')
  } catch (error) {
    alert('复制失败')
  }
}

const downloadResult = () => {
  const text = resultData.value?.content || ''
  const blob = new Blob([text], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'result.txt'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const getTimeAgo = () => {
  const now = new Date()
  const minutes = Math.floor(Math.random() * 60)
  const hours = Math.floor(Math.random() * 24)
  if (hours === 0) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  return `${Math.floor(hours / 24)}天前`
}
</script>

<style scoped>
.text-module {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.module-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.header-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.header-text h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.header-text p {
  margin: 4px 0 0;
  font-size: 14px;
  color: #64748b;
}

.tabs-container {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 20px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  background: white;
  font-size: 14px;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-btn:hover {
  border-color: #6366f1;
  color: #6366f1;
}

.tab-btn.active {
  border-color: #6366f1;
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
}

.content-area {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.input-section {
  margin-bottom: 20px;
}

.input-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.text-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 15px;
  resize: vertical;
  outline: none;
  transition: border-color 0.3s;
  min-height: 100px;
}

.text-input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.text-input::placeholder {
  color: #9ca3af;
}

.char-count {
  display: block;
  text-align: right;
  font-size: 12px;
  color: #9ca3af;
  margin-top: 6px;
}

.generate-btn {
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.generate-btn.loading {
  background: #94a3b8;
}

.result-section {
  margin-top: 24px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 10px;
}

.result-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.response-time {
  font-size: 12px;
  color: #64748b;
  background: white;
  padding: 4px 12px;
  border-radius: 20px;
}

.result-content {
  background: white;
  padding: 16px;
  border-radius: 10px;
  min-height: 100px;
  margin-bottom: 16px;
}

.result-content p {
  margin: 0;
  line-height: 1.7;
  color: #374151;
  white-space: pre-wrap;
}

.result-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-btn {
  padding: 10px 20px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  background: white;
  font-size: 14px;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  border-color: #6366f1;
  color: #6366f1;
}
</style>