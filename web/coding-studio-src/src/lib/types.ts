export type Source = 'post' | 'external';

export interface Post {
  sample_id: string;
  source_post_id?: string | null;
  posted_at?: string | null;
  post_text: string;
  text_chars?: number | null;
  author_type?: string | null;
  author_name?: string | null;
  author_headline?: string | null;
  post_url?: string | null;
  reactions?: number | null;
  comments?: number | null;
  shares?: number | null;
  has_external_link?: boolean | null;
  external_url_count?: number | null;
  newsletter_title?: string | null;
  newsletter_url?: string | null;
}

export interface ExtSource {
  id: number;
  sample_id: string;
  source_kind?: string | null;
  original_url?: string | null;
  resolved_url?: string | null;
  domain?: string | null;
  title?: string | null;
  extracted_text?: string | null;
  extracted_chars?: number | null;
  fetch_status: string;
  http_status?: number | null;
}

export interface Theme { id: number; name: string; sort_order: number }

export interface Code {
  id: number;
  label: string;
  color_idx: number;
  theme_id: number | null;
  created_at?: string;
}

export interface Highlight {
  id: number;
  sample_id: string;
  source: Source;
  external_source_id: number | null;
  paragraph_idx: number;
  start_offset: number;
  end_offset: number;
  quote: string;
  code_id: number;
  created_at?: string;
}

export type NewHighlight = Omit<Highlight, 'id' | 'created_at'>;

export interface PostStatus {
  sample_id: string;
  is_coded: boolean;
  link_reviewed: boolean;
  coder_notes: string;
}

export interface Coder {
  id: number;
  name: string;
  name_en?: string | null;
  total_posts: number;
  coded_count: number;
  codes_count: number;
  highlights_count: number;
  last_activity: string | null;
}

export interface Workspace {
  posts: Post[];
  ext: ExtSource[];
  themes: Theme[];
  codes: Code[];
  highlights: Highlight[];
  status: Record<string, PostStatus>;
}
