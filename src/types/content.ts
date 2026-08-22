export type Status =
  | '有项目实践'
  | '能够独立完成基础操作'
  | '能够排查常见问题'
  | '正在系统学习';

export interface SkillItem {
  name: string;
  direction: string;
  scenario: string;
  status: Status;
}

export interface SkillGroup {
  title: string;
  summary: string;
  items: SkillItem[];
}

export interface Project {
  slug: string;
  title: string;
  subtitle: string;
  coverTone: string;
  tags: string[];
  role: string;
  result: string;
  overview: string;
  highlights: string[];
  githubUrl: string;
}

export interface TroubleshootingCase {
  slug: string;
  title: string;
  symptom: string;
  process: string;
  tools: string[];
  rootCause: string;
  resolution: string;
  review: string;
}

export interface Article {
  slug: string;
  title: string;
  category: string;
  excerpt: string;
  date: string;
  readTime: string;
  content: string;
}

export interface TimelineItem {
  time: string;
  title: string;
  detail: string;
}

export interface SocialLinks {
  githubUrl: string;
  email: string;
  bilibiliUrl: string;
  douyinUrl: string;
  xiaohongshuUrl: string;
  resumeUrl: string;
}

export interface CapabilityCard {
  title: string;
  tech: string;
  practice: string;
}

export interface Profile {
  name: string;
  handle: string;
  title: string;
  focus: string;
  intro: string;
  location: string;
  socialLinks: SocialLinks;
  capabilityCards: CapabilityCard[];
}
