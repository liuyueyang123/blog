<script setup lang="ts">
import { ref, onMounted } from 'vue';
import AdminNav from '../components/AdminNav.vue';
import {
  getAdminSkillGroups,
  createSkillGroup,
  updateSkillGroup,
  deleteSkillGroup,
  createSkillItem,
  updateSkillItem,
  deleteSkillItem,
  SKILL_STATUS_OPTIONS,
  type SkillGroup,
  type SkillItem,
} from '../api/skills';

const groups = ref<SkillGroup[]>([]);
const loading = ref(true);

// ── 新增技能组 ──
const addingGroup = ref(false);
const newGroupForm = ref({ title: '', summary: '' });

// ── 编辑技能组 ──
const editingGroupId = ref<number | null>(null);
const groupForm = ref({ title: '', summary: '' });

// ── 新增技能项 ──
const addingItemGroupId = ref<number | null>(null);
const newItemForm = ref({ name: '', direction: '', scenario: '', status: SKILL_STATUS_OPTIONS[3] });

// ── 编辑技能项 ──
const editingItemId = ref<number | null>(null);
const itemForm = ref({ name: '', direction: '', scenario: '', status: '' });

onMounted(async () => {
  try {
    groups.value = await getAdminSkillGroups();
  } finally {
    loading.value = false;
  }
});

// ── 技能组操作 ──────────────────────────────────────────

async function handleAddGroup() {
  if (!newGroupForm.value.title.trim()) return;
  const created = await createSkillGroup({
    title: newGroupForm.value.title,
    summary: newGroupForm.value.summary,
    sort_order: groups.value.length + 1,
  });
  groups.value.push({ ...created, items: [] });
  newGroupForm.value = { title: '', summary: '' };
  addingGroup.value = false;
}

function startEditGroup(group: SkillGroup) {
  editingGroupId.value = group.id!;
  groupForm.value = { title: group.title, summary: group.summary };
}

async function handleSaveGroup(group: SkillGroup) {
  const updated = await updateSkillGroup(group.id!, {
    title: groupForm.value.title,
    summary: groupForm.value.summary,
  });
  group.title = updated.title;
  group.summary = updated.summary;
  editingGroupId.value = null;
}

async function handleDeleteGroup(group: SkillGroup) {
  if (!confirm(`确定删除技能组「${group.title}」及其 ${group.items.length} 个技能项吗？`)) return;
  await deleteSkillGroup(group.id!);
  groups.value = groups.value.filter((g) => g.id !== group.id);
}

// ── 技能项操作 ──────────────────────────────────────────

function startAddItem(group: SkillGroup) {
  addingItemGroupId.value = group.id!;
  newItemForm.value = { name: '', direction: '', scenario: '', status: SKILL_STATUS_OPTIONS[3] };
}

async function handleAddItem(group: SkillGroup) {
  if (!newItemForm.value.name.trim()) return;
  const created = await createSkillItem(group.id!, {
    name: newItemForm.value.name,
    direction: newItemForm.value.direction,
    scenario: newItemForm.value.scenario,
    status: newItemForm.value.status,
    sort_order: group.items.length + 1,
  });
  group.items.push(created);
  addingItemGroupId.value = null;
}

function startEditItem(item: SkillItem) {
  editingItemId.value = item.id!;
  itemForm.value = { name: item.name, direction: item.direction, scenario: item.scenario, status: item.status };
}

async function handleSaveItem(item: SkillItem) {
  const updated = await updateSkillItem(item.id!, { ...itemForm.value });
  item.name = updated.name;
  item.direction = updated.direction;
  item.scenario = updated.scenario;
  item.status = updated.status;
  editingItemId.value = null;
}

async function handleDeleteItem(group: SkillGroup, item: SkillItem) {
  if (!confirm(`确定删除技能「${item.name}」吗？`)) return;
  await deleteSkillItem(item.id!);
  group.items = group.items.filter((i) => i.id !== item.id);
}
</script>

<template>
  <div class="admin-container">
    <AdminNav title="技能管理">
      <template #actions>
        <button class="btn btn-primary" @click="addingGroup = !addingGroup">+ 新增技能组</button>
      </template>
    </AdminNav>

    <div v-if="loading" class="empty-state">加载中...</div>

    <template v-else>
      <!-- 新增技能组表单 -->
      <div v-if="addingGroup" class="card" style="margin-bottom: 18px">
        <div class="form-group">
          <label>组名称</label>
          <input v-model="newGroupForm.title" placeholder="例如：Linux 与基础设施" />
        </div>
        <div class="form-group">
          <label>组简介</label>
          <input v-model="newGroupForm.summary" placeholder="一句话描述这个技能组" />
        </div>
        <div style="display: flex; gap: 10px">
          <button class="btn btn-primary" @click="handleAddGroup">创建</button>
          <button class="btn" @click="addingGroup = false">取消</button>
        </div>
      </div>

      <!-- 技能组列表 -->
      <div v-for="group in groups" :key="group.id" class="card" style="margin-bottom: 18px">
        <!-- 组头：显示模式 -->
        <div v-if="editingGroupId !== group.id" style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px">
          <div>
            <h2 style="margin: 0; font-size: 18px">{{ group.title }}</h2>
            <p style="margin: 6px 0 0; color: var(--text-secondary); font-size: 13px">{{ group.summary }}</p>
          </div>
          <div style="display: flex; gap: 8px; flex-shrink: 0">
            <button class="btn btn-sm" @click="startAddItem(group)">+ 技能</button>
            <button class="btn btn-sm" @click="startEditGroup(group)">编辑组</button>
            <button class="btn btn-sm btn-danger" @click="handleDeleteGroup(group)">删除组</button>
          </div>
        </div>

        <!-- 组头：编辑模式 -->
        <div v-else>
          <div class="form-group">
            <label>组名称</label>
            <input v-model="groupForm.title" />
          </div>
          <div class="form-group">
            <label>组简介</label>
            <input v-model="groupForm.summary" />
          </div>
          <div style="display: flex; gap: 10px; margin-bottom: 16px">
            <button class="btn btn-primary btn-sm" @click="handleSaveGroup(group)">保存</button>
            <button class="btn btn-sm" @click="editingGroupId = null">取消</button>
          </div>
        </div>

        <!-- 技能项表格 -->
        <table class="table" style="margin-top: 14px">
          <thead>
            <tr>
              <th style="width: 16%">名称</th>
              <th style="width: 16%">方向</th>
              <th>使用场景</th>
              <th style="width: 15%">状态</th>
              <th style="width: 110px">操作</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="item in group.items" :key="item.id">
              <!-- 技能项：显示模式 -->
              <tr v-if="editingItemId !== item.id">
                <td>{{ item.name }}</td>
                <td>{{ item.direction }}</td>
                <td style="color: var(--text-secondary); font-size: 13px">{{ item.scenario }}</td>
                <td><span class="tag tag-published">{{ item.status }}</span></td>
                <td>
                  <button class="btn btn-sm" @click="startEditItem(item)">编辑</button>
                  <button class="btn btn-sm btn-danger" @click="handleDeleteItem(group, item)">删除</button>
                </td>
              </tr>
              <!-- 技能项：编辑模式 -->
              <tr v-else>
                <td colspan="5">
                  <div class="form-row">
                    <div class="form-group">
                      <label>名称</label>
                      <input v-model="itemForm.name" />
                    </div>
                    <div class="form-group">
                      <label>方向</label>
                      <input v-model="itemForm.direction" />
                    </div>
                  </div>
                  <div class="form-group">
                    <label>使用场景</label>
                    <input v-model="itemForm.scenario" />
                  </div>
                  <div class="form-group" style="max-width: 280px">
                    <label>状态</label>
                    <select v-model="itemForm.status">
                      <option v-for="s in SKILL_STATUS_OPTIONS" :key="s" :value="s">{{ s }}</option>
                    </select>
                  </div>
                  <div style="display: flex; gap: 10px">
                    <button class="btn btn-primary btn-sm" @click="handleSaveItem(item)">保存</button>
                    <button class="btn btn-sm" @click="editingItemId = null">取消</button>
                  </div>
                </td>
              </tr>
            </template>

            <!-- 新增技能项表单行 -->
            <tr v-if="addingItemGroupId === group.id">
              <td colspan="5">
                <div class="form-row">
                  <div class="form-group">
                    <label>名称</label>
                    <input v-model="newItemForm.name" placeholder="例如：Docker" />
                  </div>
                  <div class="form-group">
                    <label>方向</label>
                    <input v-model="newItemForm.direction" placeholder="例如：容器" />
                  </div>
                </div>
                <div class="form-group">
                  <label>使用场景</label>
                  <input v-model="newItemForm.scenario" placeholder="描述使用场景" />
                </div>
                <div class="form-group" style="max-width: 280px">
                  <label>状态</label>
                  <select v-model="newItemForm.status">
                    <option v-for="s in SKILL_STATUS_OPTIONS" :key="s" :value="s">{{ s }}</option>
                  </select>
                </div>
                <div style="display: flex; gap: 10px">
                  <button class="btn btn-primary btn-sm" @click="handleAddItem(group)">添加</button>
                  <button class="btn btn-sm" @click="addingItemGroupId = null">取消</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <p v-if="group.items.length === 0 && addingItemGroupId !== group.id" style="color: var(--text-secondary); font-size: 13px; margin: 12px 0 0">
          该组暂无技能项
        </p>
      </div>
    </template>
  </div>
</template>
