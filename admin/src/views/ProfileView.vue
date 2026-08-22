<script setup lang="ts">
import { ref, onMounted } from 'vue';
import AdminNav from '../components/AdminNav.vue';
import { getAdminProfile, updateProfile, type CapabilityCard, type ProfilePayload } from '../api/profile';

const loading = ref(true);
const saving = ref(false);
const error = ref('');

const form = ref({
  name: '',
  handle: '',
  title: '',
  focus: '',
  intro: '',
  location: '',
  github_url: '',
  email: '',
  bilibili_url: '',
  douyin_url: '',
  xiaohongshu_url: '',
  resume_url: '',
  capability_cards: [] as CapabilityCard[],
});

// ── 能力卡片内联编辑（本地操作，随整表一起保存） ──
const addingCard = ref(false);
const newCardForm = ref<CapabilityCard>({ title: '', tech: '', practice: '' });
const editingCardIndex = ref<number | null>(null);
const cardForm = ref<CapabilityCard>({ title: '', tech: '', practice: '' });

onMounted(async () => {
  try {
    const profile = await getAdminProfile();
    form.value.name = profile.name;
    form.value.handle = profile.handle;
    form.value.title = profile.title;
    form.value.focus = profile.focus;
    form.value.intro = profile.intro;
    form.value.location = profile.location;
    form.value.github_url = profile.socialLinks.githubUrl;
    form.value.email = profile.socialLinks.email;
    form.value.bilibili_url = profile.socialLinks.bilibiliUrl;
    form.value.douyin_url = profile.socialLinks.douyinUrl;
    form.value.xiaohongshu_url = profile.socialLinks.xiaohongshuUrl;
    form.value.resume_url = profile.socialLinks.resumeUrl;
    form.value.capability_cards = profile.capabilityCards.map((c) => ({ ...c }));
  } finally {
    loading.value = false;
  }
});

function handleAddCard() {
  if (!newCardForm.value.title.trim()) return;
  form.value.capability_cards.push({ ...newCardForm.value });
  newCardForm.value = { title: '', tech: '', practice: '' };
  addingCard.value = false;
}

function startEditCard(index: number) {
  editingCardIndex.value = index;
  cardForm.value = { ...form.value.capability_cards[index] };
}

function handleSaveCard(index: number) {
  form.value.capability_cards[index] = { ...cardForm.value };
  editingCardIndex.value = null;
}

function handleDeleteCard(index: number) {
  if (!confirm('确定删除这张能力卡片吗？')) return;
  form.value.capability_cards.splice(index, 1);
}

async function handleSave() {
  error.value = '';
  saving.value = true;
  const payload: ProfilePayload = {
    name: form.value.name,
    handle: form.value.handle,
    title: form.value.title,
    focus: form.value.focus,
    intro: form.value.intro,
    location: form.value.location,
    github_url: form.value.github_url,
    email: form.value.email,
    bilibili_url: form.value.bilibili_url,
    douyin_url: form.value.douyin_url,
    xiaohongshu_url: form.value.xiaohongshu_url,
    resume_url: form.value.resume_url,
    capability_cards: form.value.capability_cards,
  };
  try {
    await updateProfile(payload);
  } catch (e: any) {
    error.value = e.response?.data?.detail || '保存失败';
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <div class="admin-container">
    <AdminNav title="个人资料管理" />

    <div v-if="loading" class="empty-state">加载中...</div>

    <form v-else class="card" @submit.prevent="handleSave">
      <div class="form-row">
        <div class="form-group">
          <label>姓名</label>
          <input v-model="form.name" />
        </div>
        <div class="form-group">
          <label>Handle</label>
          <input v-model="form.handle" />
        </div>
      </div>

      <div class="form-group">
        <label>头衔</label>
        <input v-model="form.title" placeholder="Linux / Cloud / SRE / AI Engineering" />
      </div>

      <div class="form-group">
        <label>关注方向</label>
        <input v-model="form.focus" />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>位置</label>
          <input v-model="form.location" />
        </div>
        <div class="form-group">
          <label>简历链接</label>
          <input v-model="form.resume_url" placeholder="/resume/resume-placeholder.pdf" />
        </div>
      </div>

      <div class="form-group">
        <label>个人介绍</label>
        <textarea v-model="form.intro" rows="3"></textarea>
      </div>

      <h2 style="margin: 24px 0 12px; font-size: 16px">社交链接</h2>
      <div class="form-row">
        <div class="form-group">
          <label>GitHub</label>
          <input v-model="form.github_url" />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="form.email" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>B 站</label>
          <input v-model="form.bilibili_url" />
        </div>
        <div class="form-group">
          <label>抖音</label>
          <input v-model="form.douyin_url" />
        </div>
        <div class="form-group">
          <label>小红书</label>
          <input v-model="form.xiaohongshu_url" />
        </div>
      </div>

      <h2 style="margin: 24px 0 12px; font-size: 16px">
        能力卡片
        <button class="btn btn-primary btn-sm" type="button" style="margin-left: 10px" @click="addingCard = !addingCard">
          + 新增卡片
        </button>
      </h2>

      <!-- 新增能力卡片 -->
      <div v-if="addingCard" class="card" style="margin-bottom: 12px; background: rgba(255,255,255,0.02)">
        <div class="form-row">
          <div class="form-group">
            <label>标题</label>
            <input v-model="newCardForm.title" placeholder="例如：Linux 与云计算" />
          </div>
          <div class="form-group">
            <label>技术栈</label>
            <input v-model="newCardForm.tech" placeholder="Linux, Shell, Nginx, MySQL" />
          </div>
        </div>
        <div class="form-group">
          <label>实践描述</label>
          <input v-model="newCardForm.practice" placeholder="一句话描述实践" />
        </div>
        <div style="display: flex; gap: 10px">
          <button class="btn btn-primary btn-sm" type="button" @click="handleAddCard">添加</button>
          <button class="btn btn-sm" type="button" @click="addingCard = false">取消</button>
        </div>
      </div>

      <!-- 能力卡片列表 -->
      <div v-for="(card, index) in form.capability_cards" :key="index" class="card" style="margin-bottom: 12px">
        <div v-if="editingCardIndex !== index" style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px">
          <div>
            <strong>{{ card.title }}</strong>
            <p style="margin: 6px 0 0; color: var(--text-secondary); font-size: 13px">{{ card.tech }}</p>
            <p style="margin: 4px 0 0; color: var(--text-secondary); font-size: 13px">{{ card.practice }}</p>
          </div>
          <div style="display: flex; gap: 8px; flex-shrink: 0">
            <button class="btn btn-sm" type="button" @click="startEditCard(index)">编辑</button>
            <button class="btn btn-sm btn-danger" type="button" @click="handleDeleteCard(index)">删除</button>
          </div>
        </div>
        <div v-else>
          <div class="form-row">
            <div class="form-group">
              <label>标题</label>
              <input v-model="cardForm.title" />
            </div>
            <div class="form-group">
              <label>技术栈</label>
              <input v-model="cardForm.tech" />
            </div>
          </div>
          <div class="form-group">
            <label>实践描述</label>
            <input v-model="cardForm.practice" />
          </div>
          <div style="display: flex; gap: 10px">
            <button class="btn btn-primary btn-sm" type="button" @click="handleSaveCard(index)">保存</button>
            <button class="btn btn-sm" type="button" @click="editingCardIndex = null">取消</button>
          </div>
        </div>
      </div>

      <div style="display: flex; gap: 12px; margin-top: 8px">
        <button class="btn btn-primary" type="submit" :disabled="saving">
          {{ saving ? '保存中...' : '保存' }}
        </button>
      </div>
      <p v-if="error" class="error-msg">{{ error }}</p>
    </form>
  </div>
</template>
