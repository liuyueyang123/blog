<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import AdminNav from '../components/AdminNav.vue';
import { getAdminProjects, deleteProject, type Project } from '../api/projects';

const projects = ref<Project[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    projects.value = await getAdminProjects();
  } finally {
    loading.value = false;
  }
});

async function handleDelete(project: Project) {
  if (!confirm(`确定删除项目「${project.title}」吗？`)) return;
  await deleteProject(project.id!);
  projects.value = projects.value.filter((p) => p.id !== project.id);
}
</script>

<template>
  <div class="admin-container">
    <AdminNav title="项目管理">
      <template #actions>
        <RouterLink class="btn btn-primary" to="/projects/new">+ 新增项目</RouterLink>
      </template>
    </AdminNav>

    <div v-if="loading" class="empty-state">加载中...</div>

    <div v-else-if="projects.length === 0" class="empty-state">暂无项目</div>

    <table v-else class="table card" style="padding: 0">
      <thead>
        <tr>
          <th>标题</th>
          <th>封面</th>
          <th>标签数</th>
          <th>状态</th>
          <th style="width: 140px">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="project in projects" :key="project.id">
          <td>{{ project.title }}</td>
          <td>{{ project.coverTone }}</td>
          <td>{{ project.tags.length }}</td>
          <td>
            <span class="tag" :class="project.isPublished ? 'tag-published' : 'tag-draft'">
              {{ project.isPublished ? '已发布' : '草稿' }}
            </span>
          </td>
          <td>
            <RouterLink class="btn btn-sm" :to="`/projects/${project.id}/edit`">编辑</RouterLink>
            <button class="btn btn-sm btn-danger" @click="handleDelete(project)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
