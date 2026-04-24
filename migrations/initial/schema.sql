-- Generated from ../solid-sheep/lib/staging-schema-sql.js for TKT-019.

-- Source snapshot: 251 CREATE TABLE statements in the current staging schema export.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE entities (
  id TEXT PRIMARY KEY,
  legal_name TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ('holding','subsidiary','fund','spv','portfolio')),
  jurisdiction TEXT DEFAULT 'Delaware',
  parent_entity_id TEXT REFERENCES entities(id),
  status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','inactive','dissolved')),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE people (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('admin','partner','team','investor','advisor')),
  tier TEXT NOT NULL CHECK(tier IN ('partner','team','investor','advisor')),
  title TEXT,
  division TEXT,
  entity_access JSONB NOT NULL DEFAULT '[]'::jsonb,
  scopes JSONB NOT NULL DEFAULT '[]'::jsonb,
  agents JSONB NOT NULL DEFAULT '[]'::jsonb,
  default_agent TEXT,
  status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','inactive','offboarded')),
  avatar_url TEXT,
  monitoring_tier TEXT NOT NULL DEFAULT 'signals' CHECK(monitoring_tier IN ('signals','summarized','raw')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  photo_url TEXT,
  department TEXT,
  is_workspace_admin INTEGER DEFAULT 0,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE clients (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  entity_id TEXT NOT NULL REFERENCES entities(id),
  owner TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','churned','prospect','paused')),
  health TEXT NOT NULL DEFAULT 'healthy' CHECK(health IN ('healthy','watch','at_risk','critical')),
  monthly_value DOUBLE PRECISION DEFAULT 0,
  margin_pct DOUBLE PRECISION DEFAULT 0,
  renewal_date TEXT,
  last_touch TEXT,
  next_action TEXT,
  next_action_date TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  stripe_customer_id TEXT
);

CREATE TABLE client_contacts (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  email TEXT,
  phone TEXT,
  role TEXT,
  is_primary INTEGER NOT NULL DEFAULT 0,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE investors (
  id TEXT PRIMARY KEY,
  pipeline_type TEXT NOT NULL CHECK(pipeline_type IN ('lp_fundraise','sm_investors','sales','osma_customers','recruiting')),
  name TEXT NOT NULL,
  firm TEXT,
  email TEXT,
  phone TEXT,
  entity_id TEXT NOT NULL REFERENCES entities(id),
  owner TEXT NOT NULL,
  stage TEXT NOT NULL,
  persona TEXT,
  amount DOUBLE PRECISION DEFAULT 0,
  last_touch TEXT,
  next_action TEXT,
  next_action_date TEXT,
  notes TEXT,
  tags TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  investor_profile_id TEXT,
  crm_contact_id TEXT,
  crm_company_id TEXT,
  pipeline_deal_id TEXT,
  raise_id TEXT,
  engagement_score INTEGER DEFAULT 0
);

CREATE TABLE deals (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  entity_id TEXT NOT NULL REFERENCES entities(id),
  owner TEXT NOT NULL,
  type TEXT DEFAULT 'investment',
  stage TEXT NOT NULL,
  amount DOUBLE PRECISION DEFAULT 0,
  probability DOUBLE PRECISION DEFAULT 0,
  close_date TEXT,
  counterparty TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE initiatives (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  entity_id TEXT NOT NULL REFERENCES entities(id),
  division TEXT,
  owner TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'planning' CHECK(status IN ('planning','in_progress','blocked','complete','on_hold')),
  health TEXT NOT NULL DEFAULT 'on_track' CHECK(health IN ('on_track','watch','at_risk','critical')),
  current_milestone TEXT,
  next_action TEXT,
  next_action_date TEXT,
  target_date TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  labs_visible INTEGER DEFAULT 0,
  labs_stage TEXT DEFAULT 'discovery' CHECK(labs_stage IN ('discovery','preview','beta','active')),
  labs_section TEXT,
  labs_tagline TEXT,
  labs_description TEXT,
  labs_icon TEXT,
  labs_color TEXT,
  labs_url TEXT,
  labs_waitlist_url TEXT,
  labs_demo_type TEXT CHECK(labs_demo_type IS NULL OR labs_demo_type IN ('jsx','iframe','video','screenshots')),
  labs_demo_source TEXT,
  labs_sort_order INTEGER DEFAULT 0,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE milestones (
  id TEXT PRIMARY KEY,
  initiative_id TEXT NOT NULL REFERENCES initiatives(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','in_progress','complete','blocked')),
  due_date TEXT,
  completed_date TEXT,
  owner TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  owner TEXT NOT NULL,
  entity_id TEXT NOT NULL REFERENCES entities(id),
  initiative_id TEXT REFERENCES initiatives(id),
  priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low','medium','high','critical')),
  status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','in_progress','done','blocked','deferred')),
  due_date TEXT,
  source TEXT NOT NULL DEFAULT 'manual' CHECK(source IN ('manual','agent','meeting','email')),
  source_agent TEXT,
  requires_approval INTEGER NOT NULL DEFAULT 0,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  chain_id TEXT
);

CREATE TABLE decisions (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  entity_id TEXT NOT NULL REFERENCES entities(id),
  owners TEXT NOT NULL,
  decision_text TEXT NOT NULL,
  options_considered TEXT,
  rationale TEXT,
  impact TEXT,
  follow_ups JSONB,
  sources TEXT,
  status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN ('draft','pending','final','reversed')),
  decided_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE approvals (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ('cash','client_commitment','legal','governance','hr','investor_comms','execution')),
  entity_id TEXT NOT NULL REFERENCES entities(id),
  source_agent TEXT,
  requested_by TEXT NOT NULL DEFAULT 'system',
  assigned_to TEXT NOT NULL,
  risk_level TEXT NOT NULL DEFAULT 'medium' CHECK(risk_level IN ('low','medium','high','critical')),
  summary TEXT NOT NULL,
  detail TEXT,
  status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','approved','rejected','expired')),
  decided_at TIMESTAMPTZ,
  decided_by TEXT,
  decision_comment TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE documents (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  category TEXT NOT NULL CHECK(category IN ('compensation','governance','operations','fund','tax','clients','onboarding','legal')),
  entity_id TEXT NOT NULL REFERENCES entities(id),
  owner TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'current' CHECK(status IN ('current','needs_review','pending','draft','archived')),
  doc_url TEXT,
  next_action TEXT,
  next_action_date TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE governance (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ('board_consent','filing','compliance','tax_deadline','reporting')),
  entity_id TEXT NOT NULL REFERENCES entities(id),
  owner TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','in_progress','complete','overdue','blocked')),
  due_date TEXT,
  completed_date TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE finance_snapshots (
  id TEXT PRIMARY KEY,
  entity_id TEXT NOT NULL REFERENCES entities(id),
  period TEXT NOT NULL,
  cash_position DOUBLE PRECISION DEFAULT 0,
  revenue_monthly DOUBLE PRECISION DEFAULT 0,
  burn_monthly DOUBLE PRECISION DEFAULT 0,
  runway_months DOUBLE PRECISION DEFAULT 0,
  ar_outstanding DOUBLE PRECISION DEFAULT 0,
  ap_outstanding DOUBLE PRECISION DEFAULT 0,
  headcount INTEGER DEFAULT 0,
  rev_per_employee DOUBLE PRECISION DEFAULT 0,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE events (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL CHECK(type IN ('object_created','object_updated','approval_completed','brief_generated','ask_query','team_signal_access','raw_access')),
  entity_id TEXT,
  actor TEXT NOT NULL,
  target_type TEXT,
  target_id TEXT,
  detail TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE team_signals (
  id TEXT PRIMARY KEY,
  person_email TEXT NOT NULL,
  period TEXT NOT NULL,
  signal TEXT NOT NULL DEFAULT 'healthy' CHECK(signal IN ('healthy','watch','concerning')),
  signal_color TEXT NOT NULL DEFAULT 'green' CHECK(signal_color IN ('green','amber','red')),
  summary TEXT,
  slack_activity_trend DOUBLE PRECISION DEFAULT 0,
  last_project_update_days INTEGER DEFAULT 0,
  last_client_touch_days INTEGER DEFAULT 0,
  tasks_completed_this_week INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notes (
  id TEXT PRIMARY KEY,
  target_type TEXT NOT NULL,
  target_id TEXT NOT NULL,
  author TEXT NOT NULL,
  content TEXT NOT NULL,
  is_private INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE connector_configs (
  id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'disconnected',
  connected_by TEXT,
  connected_at TIMESTAMPTZ,
  last_sync TEXT,
  sync_frequency INTEGER DEFAULT 15,
  settings JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  sync_count INTEGER DEFAULT 0,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE sync_log (
  id TEXT PRIMARY KEY,
  connector_id TEXT NOT NULL,
  started_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'running',
  records_synced INTEGER DEFAULT 0,
  error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (connector_id) REFERENCES connector_configs(id)
);

CREATE TABLE calendar_events (
  id TEXT PRIMARY KEY,
  connector_id TEXT NOT NULL,
  event_id TEXT NOT NULL,
  title TEXT,
  start_time TEXT,
  end_time TEXT,
  attendees TEXT,
  location TEXT,
  description TEXT,
  entity_id TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  listener_processed INTEGER DEFAULT 0
);

CREATE TABLE qb_transactions (
  id TEXT PRIMARY KEY,
  connector_id TEXT NOT NULL,
  txn_id TEXT NOT NULL,
  type TEXT,
  date TEXT,
  amount DOUBLE PRECISION,
  account TEXT,
  entity_id TEXT,
  description TEXT,
  raw_json JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  hub_category_confidence DOUBLE PRECISION DEFAULT 0,
  vendor TEXT
);

CREATE TABLE investor_users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  investor_id TEXT NOT NULL,
  name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE investor_updates (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  date TEXT NOT NULL,
  visibility TEXT NOT NULL DEFAULT 'all',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fund_metrics (
  id TEXT PRIMARY KEY,
  period TEXT NOT NULL,
  fund_size DOUBLE PRECISION NOT NULL DEFAULT 0,
  committed DOUBLE PRECISION NOT NULL DEFAULT 0,
  deployed DOUBLE PRECISION NOT NULL DEFAULT 0,
  distributions DOUBLE PRECISION NOT NULL DEFAULT 0,
  irr DOUBLE PRECISION DEFAULT NULL,
  tvpi DOUBLE PRECISION DEFAULT NULL,
  dpi DOUBLE PRECISION DEFAULT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fund_documents (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  description TEXT,
  doc_url TEXT,
  file_name TEXT,
  visibility TEXT NOT NULL DEFAULT 'all',
  published_date TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE investor_transactions (
  id TEXT PRIMARY KEY,
  investor_id TEXT NOT NULL,
  type TEXT NOT NULL,
  amount DOUBLE PRECISION NOT NULL,
  date TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'completed',
  description TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE client_users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  client_id TEXT NOT NULL,
  name TEXT NOT NULL,
  role TEXT DEFAULT 'Client Contact',
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE client_messages (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  sender_email TEXT NOT NULL,
  sender_name TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_internal INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE client_invoices (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  number TEXT,
  amount DOUBLE PRECISION NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'draft',
  date TEXT,
  due_date TEXT,
  paid_date TEXT,
  qb_invoice_id TEXT,
  description TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  stripe_invoice_id TEXT,
  stripe_customer_id TEXT
);

CREATE TABLE brief_preferences (
  email TEXT PRIMARY KEY NOT NULL,
  daily_enabled INTEGER NOT NULL DEFAULT 1,
  weekly_enabled INTEGER NOT NULL DEFAULT 1,
  delivery_time TEXT NOT NULL DEFAULT '07:00',
  timezone TEXT NOT NULL DEFAULT 'America/Chicago',
  format TEXT NOT NULL DEFAULT 'full',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE brief_deliveries (
  id TEXT PRIMARY KEY NOT NULL,
  user_email TEXT NOT NULL,
  type TEXT NOT NULL,
  status TEXT NOT NULL,
  error TEXT,
  resend_id TEXT,
  delivered_at TIMESTAMPTZ NOT NULL,
  FOREIGN KEY (user_email) REFERENCES people(email)
);

CREATE TABLE ask_conversations (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  agents_json JSONB DEFAULT '[]'::jsonb
);

CREATE TABLE ask_messages (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  sources_json JSONB,
  agent TEXT,
  model TEXT,
  confidence TEXT CHECK(confidence IN ('high', 'medium', 'low') OR confidence IS NULL),
  follow_ups_json JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (conversation_id) REFERENCES ask_conversations(id)
);

CREATE TABLE team_signal_history (
  id TEXT NOT NULL PRIMARY KEY,
  person_email TEXT NOT NULL,
  date TEXT NOT NULL,
  signal TEXT NOT NULL,
  metrics_json JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  UNIQUE(person_email, date)
);

CREATE TABLE email_templates (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  subject_template TEXT NOT NULL,
  body_template TEXT NOT NULL,
  category TEXT NOT NULL DEFAULT 'general',
  entity_id TEXT,
  created_by TEXT,
  variables_json JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ask_actions (
  id TEXT PRIMARY KEY,
  conversation_id TEXT,
  message_id TEXT,
  action_type TEXT NOT NULL,
  action_params_json JSONB,
  status TEXT NOT NULL DEFAULT 'proposed',
  confirmed_by TEXT,
  confirmed_at TIMESTAMPTZ,
  executed_at TIMESTAMPTZ,
  result_json JSONB,
  error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_preferences (
  id TEXT PRIMARY KEY,
  user_email TEXT UNIQUE NOT NULL,
  default_view TEXT DEFAULT 'brief',
  sidebar_order_json JSONB,
  brief_emphasis_json JSONB,
  notification_filters_json JSONB,
  dashboard_layout_json JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  agent_domains JSONB,
  pinned_items JSONB DEFAULT '[]'::jsonb,
  tenant_id TEXT DEFAULT 'sprint_mode',
  vault_pin TEXT,
  onboarding_completed INTEGER NOT NULL DEFAULT 0,
  display_settings JSONB,
  agent_sort_pref TEXT DEFAULT 'recent',
  pinned_agents JSONB DEFAULT '[]'::jsonb,
  hide_inactive_agents INTEGER DEFAULT 0,
  team_tour_completed INTEGER DEFAULT 0,
  team_tour_data JSONB DEFAULT '{}'::jsonb,
  last_brief_generated TEXT
);

CREATE TABLE candidates (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT,
  phone TEXT,
  role_title TEXT,
  department TEXT,
  entity_id TEXT,
  stage TEXT NOT NULL DEFAULT 'sourced',
  source TEXT,
  resume_url TEXT,
  linkedin_url TEXT,
  notes TEXT,
  owner TEXT,
  jockey_score INTEGER DEFAULT 0,
  tags TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workflows (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  entity_id TEXT,
  trigger_type TEXT NOT NULL,
  trigger_config_json JSONB DEFAULT '{}'::jsonb,
  actions_json JSONB DEFAULT '{}'::jsonb,
  status TEXT NOT NULL DEFAULT 'active',
  created_by TEXT,
  last_triggered_at TIMESTAMPTZ,
  run_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workflow_runs (
  id TEXT PRIMARY KEY,
  workflow_id TEXT NOT NULL,
  trigger_event TEXT,
  actions_executed_json JSONB,
  status TEXT NOT NULL DEFAULT 'running',
  error TEXT,
  started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMPTZ,
  workflow_type TEXT,
  triggered_by TEXT,
  steps TEXT,
  current_step INTEGER DEFAULT 0,
  context TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cap_table_entries (
  id TEXT PRIMARY KEY,
  investor_profile_id TEXT,
  name TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ('founder','eip','preferred','available')),
  class TEXT NOT NULL,
  units INTEGER NOT NULL DEFAULT 0,
  invested_amount INTEGER NOT NULL DEFAULT 0,
  post_pref_pct DOUBLE PRECISION NOT NULL DEFAULT 0,
  post_eip_pct DOUBLE PRECISION NOT NULL DEFAULT 0,
  voting_pct DOUBLE PRECISION NOT NULL DEFAULT 0,
  vesting TEXT,
  note TEXT,
  portal_visible INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE portfolio_companies (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ('labs_spinout','foundry_equity','other_investment')),
  sector TEXT,
  stage TEXT,
  founded TEXT,
  sprint_investment INTEGER DEFAULT 0,
  sprint_ownership_pct DOUBLE PRECISION DEFAULT 0,
  sprint_equity_pct DOUBLE PRECISION DEFAULT 0,
  cost_basis INTEGER DEFAULT 0,
  current_valuation INTEGER DEFAULT 0,
  sprint_position_value INTEGER DEFAULT 0,
  mrr INTEGER DEFAULT 0,
  status TEXT DEFAULT 'active',
  milestone TEXT,
  notes TEXT,
  carta_fund_id TEXT,
  last_valuation_date TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ir_calendar_items (
  id TEXT PRIMARY KEY,
  category TEXT NOT NULL CHECK(category IN ('recurring','curated')),
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  period TEXT,
  due_date TEXT,
  review_by TEXT,
  status TEXT NOT NULL DEFAULT 'not_started',
  owner_user_id TEXT,
  owner_name TEXT,
  ai_suggested INTEGER NOT NULL DEFAULT 0,
  trigger_description TEXT,
  note TEXT,
  scheduled_for TEXT,
  published_at TIMESTAMPTZ,
  content_item_id TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content_items (
  id TEXT PRIMARY KEY,
  ir_calendar_item_id TEXT,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT,
  body_html TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  author_user_id TEXT,
  author_name TEXT,
  required_approvals INTEGER NOT NULL DEFAULT 1,
  current_approvals INTEGER NOT NULL DEFAULT 0,
  scheduled_for TEXT,
  published_at TIMESTAMPTZ,
  target_audience TEXT DEFAULT 'all',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content_approvals (
  id TEXT PRIMARY KEY,
  content_item_id TEXT NOT NULL,
  approver_user_id TEXT NOT NULL,
  approver_name TEXT NOT NULL,
  action TEXT NOT NULL CHECK(action IN ('approve','reject','request_changes')),
  comment TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comms_threads (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL CHECK(type IN ('announcement','qna','private')),
  title TEXT,
  pinned INTEGER NOT NULL DEFAULT 0,
  status TEXT DEFAULT 'active',
  created_by TEXT,
  target_investors TEXT DEFAULT 'all',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comms_messages (
  id TEXT PRIMARY KEY,
  thread_id TEXT NOT NULL,
  sender_user_id TEXT,
  sender_name TEXT NOT NULL,
  sender_type TEXT NOT NULL CHECK(sender_type IN ('admin','investor')),
  body TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE asks (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL CHECK(type IN ('intro','advice','fundraise','co_invest','other')),
  title TEXT NOT NULL,
  description TEXT,
  target TEXT DEFAULT 'all',
  target_investor_ids TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  created_by TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ask_responses (
  id TEXT PRIMARY KEY,
  ask_id TEXT NOT NULL,
  investor_profile_id TEXT NOT NULL,
  investor_name TEXT NOT NULL,
  body TEXT,
  status TEXT DEFAULT 'responded',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE portal_activity_log (
  id TEXT PRIMARY KEY,
  investor_profile_id TEXT NOT NULL,
  action TEXT NOT NULL,
  detail TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jockey_sessions (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN ('draft','queued','running','verifying','passed','failed','deployed')),
  automation_level INTEGER DEFAULT 1 CHECK(automation_level IN (1,2,3)),
  operator_id TEXT,
  prompt_template_version TEXT,
  skills_loaded TEXT,
  scope_files_planned TEXT,
  scope_files_actual TEXT,
  scope_violation INTEGER DEFAULT 0,
  verification_result TEXT CHECK(verification_result IS NULL OR verification_result IN ('pass','fail','partial','skipped')),
  verification_output TEXT,
  token_usage INTEGER,
  cost_usd DOUBLE PRECISION,
  duration_seconds INTEGER,
  error_class TEXT CHECK(error_class IS NULL OR error_class IN ('path_error','build_error','test_error','deploy_error','scope_error','timeout')),
  error_detail TEXT,
  prompt_text TEXT,
  session_log TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  deployed_at TIMESTAMPTZ,
  delivery_target TEXT DEFAULT 'internal',
  client_email TEXT,
  execution_mode TEXT DEFAULT 'local' CHECK (execution_mode IN ('local','cloud','text_only')),
  model TEXT DEFAULT 'claude-sonnet-4-6',
  created_by TEXT,
  deploy_approved_by TEXT,
  deploy_approved_at TIMESTAMPTZ,
  pr_url TEXT,
  branch_name TEXT,
  files_changed INTEGER DEFAULT 0,
  lines_added INTEGER DEFAULT 0,
  lines_removed INTEGER DEFAULT 0,
  commit_hash TEXT,
  smoke_pass_count INTEGER,
  smoke_total_count INTEGER,
  chain_id TEXT,
  chain_index INTEGER
);

CREATE TABLE jockey_decisions (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  session_id TEXT,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  options TEXT,
  recommendation TEXT,
  priority TEXT DEFAULT 'normal' CHECK(priority IN ('low','normal','high','blocking')),
  assigned_to TEXT,
  status TEXT DEFAULT 'open' CHECK(status IN ('open','decided','deferred','obsolete')),
  decision TEXT,
  decided_by TEXT,
  decided_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jockey_skills (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  project_id TEXT,
  type TEXT NOT NULL CHECK(type IN ('base','project','task')),
  description TEXT,
  file_path TEXT NOT NULL,
  success_rate DOUBLE PRECISION,
  avg_duration_seconds INTEGER,
  total_uses INTEGER DEFAULT 0,
  last_used_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jockey_evals (
  id TEXT PRIMARY KEY,
  eval_date TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ('daily','weekly','cc_release','manual')),
  findings TEXT NOT NULL,
  actions_taken JSONB,
  actions_pending TEXT,
  metrics TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jockey_patterns (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  source_project_id TEXT,
  category TEXT CHECK(category IS NULL OR category IN ('auth','api','deploy','database','ui','testing','integration')),
  description TEXT NOT NULL,
  pattern_content TEXT NOT NULL,
  adopted_by TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ( 'approval_needed', 'approval_completed', 'client_alert', 'governance_deadline', 'pipeline_update', 'brief_ready', 'team_signal', 'system', 'jockey_session', 'jockey_decision', 'jockey_eval', 'jockey_deploy', 'jockey_cost' )),
  title TEXT NOT NULL,
  body TEXT,
  action_url TEXT,
  is_read INTEGER NOT NULL DEFAULT 0,
  entity_id TEXT,
  source TEXT NOT NULL DEFAULT 'system',
  created_at TIMESTAMPTZ NOT NULL,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE notification_preferences (
  email TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ( 'approval_needed', 'approval_completed', 'client_alert', 'governance_deadline', 'pipeline_update', 'brief_ready', 'team_signal', 'system', 'jockey_session', 'jockey_decision', 'jockey_eval', 'jockey_deploy', 'jockey_cost' )),
  in_app INTEGER NOT NULL DEFAULT 1,
  push_email INTEGER NOT NULL DEFAULT 0,
  sound INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (email, type)
);

CREATE TABLE ir_communications (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL DEFAULT 'update',
  title TEXT NOT NULL,
  content TEXT,
  audience TEXT DEFAULT 'all',
  status TEXT DEFAULT 'published',
  published_at TIMESTAMPTZ,
  created_by TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE emails (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  subject TEXT,
  from_addr TEXT,
  to_addr TEXT,
  snippet TEXT,
  body TEXT,
  received_at TIMESTAMPTZ,
  labels TEXT,
  highlight INTEGER DEFAULT 0,
  is_read INTEGER DEFAULT 1,
  entity_id TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  gmail_message_id TEXT,
  gmail_thread_id TEXT,
  reply_status TEXT DEFAULT 'none',
  replied_by TEXT,
  replied_at TIMESTAMPTZ,
  outbound_email_id TEXT,
  listener_processed INTEGER DEFAULT 0
);

CREATE TABLE slack_messages (
  id TEXT PRIMARY KEY,
  channel TEXT NOT NULL,
  sender TEXT,
  text TEXT,
  highlight INTEGER DEFAULT 0,
  sent_at TIMESTAMPTZ,
  entity_id TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  triage_status TEXT DEFAULT 'unprocessed',
  triage_classification TEXT,
  triage_run_id TEXT
);

CREATE TABLE connectors (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  provider TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'disconnected',
  last_sync TEXT,
  config_json JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE studios_engagements (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  client_name TEXT NOT NULL,
  engagement_name TEXT NOT NULL,
  delivery_method TEXT NOT NULL CHECK (delivery_method IN ('human', 'jockey', 'hybrid')),
  monthly_revenue DOUBLE PRECISION NOT NULL DEFAULT 0,
  monthly_cogs DOUBLE PRECISION NOT NULL DEFAULT 0,
  headcount DOUBLE PRECISION DEFAULT 0,
  jockey_sessions_month INTEGER DEFAULT 0,
  jockey_cost_month DOUBLE PRECISION DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'paused', 'churned', 'prospect')),
  start_date TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE entity_status (
  id TEXT PRIMARY KEY,
  entity_name TEXT NOT NULL,
  entity_type TEXT NOT NULL CHECK (entity_type IN ('holding', 'division', 'fund', 'spinout', 'product')),
  owner TEXT NOT NULL,
  cash_position DOUBLE PRECISION,
  monthly_burn DOUBLE PRECISION,
  runway_months DOUBLE PRECISION,
  status TEXT NOT NULL CHECK (status IN ('active', 'building', 'fundraising', 'paused', 'at_risk')),
  health TEXT NOT NULL CHECK (health IN ('on_track', 'watch', 'at_risk', 'critical')),
  current_milestone TEXT,
  next_action TEXT,
  next_action_owner TEXT,
  blockers TEXT,
  notes TEXT,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE fundraise_tracking (
  id TEXT PRIMARY KEY,
  entity_id TEXT NOT NULL,
  raise_name TEXT NOT NULL,
  target_amount DOUBLE PRECISION NOT NULL,
  committed_amount DOUBLE PRECISION NOT NULL DEFAULT 0,
  owner TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('active', 'at_risk', 'closed', 'abandoned', 'paused')),
  stage TEXT NOT NULL CHECK (stage IN ('preparing', 'outreach', 'diligence', 'term_sheet', 'closing', 'closed')),
  vehicle TEXT CHECK (vehicle IN ('pref_stock', 'seed', 'series_a', 'lp_fund', 'safe', 'convertible')),
  deadline TEXT,
  next_action TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE expense_breakdown (
  id TEXT PRIMARY KEY,
  period TEXT NOT NULL,
  category TEXT NOT NULL CHECK (category IN ('cogs_contractors', 'cogs_tools', 'partner_comp', 'legal', 'bookkeeping', 'cpa', 'software', 'office', 'marketing', 'travel', 'debt_optic', 'investments', 'other')),
  vendor TEXT,
  amount DOUBLE PRECISION NOT NULL,
  notes TEXT,
  replaceable_by_hub INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE agent_configs (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  system_prompt TEXT NOT NULL,
  data_tables JSONB DEFAULT '[]'::jsonb,
  tools JSONB DEFAULT '[]'::jsonb,
  trigger_schedule TEXT,
  sidebar_section TEXT,
  default_autonomy_level INTEGER DEFAULT 3,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tier INTEGER DEFAULT 3,
  display_name TEXT,
  category TEXT DEFAULT 'operations',
  works_with JSONB DEFAULT '[]'::jsonb,
  depends_on JSONB DEFAULT '[]'::jsonb,
  serves_roles JSONB DEFAULT '[]'::jsonb,
  icon TEXT,
  productizable INTEGER DEFAULT 0,
  product_category TEXT,
  status_summary TEXT,
  tenant_id TEXT DEFAULT 'sprint_mode',
  max_daily_tokens INTEGER DEFAULT 50000,
  model TEXT DEFAULT 'claude-sonnet-4-6',
  mcp_permissions JSONB DEFAULT '[]'::jsonb,
  thinking_budget INTEGER,
  sidebar_sections JSONB,
  required_tools JSONB DEFAULT '[]'::jsonb,
  max_access_tier INTEGER DEFAULT 1,
  knowledge_domains TEXT DEFAULT 'global'
);

CREATE TABLE agent_runs (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  trigger TEXT NOT NULL DEFAULT 'manual',
  input TEXT,
  output TEXT,
  recommendations JSONB DEFAULT '[]'::jsonb,
  actions_taken JSONB DEFAULT '[]'::jsonb,
  autonomy_level_used INTEGER DEFAULT 3,
  user_feedback TEXT,
  cost_usd DOUBLE PRECISION DEFAULT 0,
  duration_ms INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  action_taken INTEGER DEFAULT 0,
  awaiting_approval INTEGER DEFAULT 0,
  actioned_at TIMESTAMPTZ,
  title TEXT,
  body TEXT,
  summary TEXT,
  priority INTEGER DEFAULT 5,
  undoable INTEGER DEFAULT 0,
  actions_json JSONB,
  autonomy_level INTEGER DEFAULT 3,
  tenant_id TEXT DEFAULT 'sprint_mode',
  conversation_id TEXT,
  visibility TEXT DEFAULT 'shared',
  snoozed_until TIMESTAMPTZ,
  dismissed INTEGER DEFAULT 0,
  artifact_id TEXT,
  compliance_flags JSONB,
  attachments_json JSONB DEFAULT '[]'::jsonb,
  FOREIGN KEY (agent_id) REFERENCES agent_configs(id)
);

CREATE TABLE agent_memory (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  entity_type TEXT,
  entity_id TEXT,
  memory_type TEXT NOT NULL DEFAULT 'observation',
  content TEXT NOT NULL,
  confidence DOUBLE PRECISION DEFAULT 0.8,
  source TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMPTZ,
  tenant_id TEXT DEFAULT 'sprint_mode',
  user_email TEXT,
  is_active INTEGER DEFAULT 1,
  FOREIGN KEY (agent_id) REFERENCES agent_configs(id)
);

CREATE TABLE autonomy_scores (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  user_email TEXT NOT NULL,
  total_actions INTEGER DEFAULT 0,
  approved_unchanged INTEGER DEFAULT 0,
  approved_edited INTEGER DEFAULT 0,
  rejected INTEGER DEFAULT 0,
  avg_edit_distance DOUBLE PRECISION DEFAULT 0,
  current_level INTEGER DEFAULT 3,
  level_up_eligible INTEGER DEFAULT 0,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  FOREIGN KEY (agent_id) REFERENCES agent_configs(id),
  UNIQUE(agent_id, action_type, user_email)
);

CREATE TABLE filing_deadlines (
  id TEXT PRIMARY KEY,
  entity TEXT NOT NULL,
  filing_type TEXT NOT NULL,
  description TEXT,
  due_date TEXT NOT NULL,
  status TEXT DEFAULT 'upcoming',
  owner TEXT,
  reminder_sent_30d INTEGER DEFAULT 0,
  reminder_sent_14d INTEGER DEFAULT 0,
  reminder_sent_7d INTEGER DEFAULT 0,
  reminder_sent_1d INTEGER DEFAULT 0,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE financial_scenarios (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  assumptions JSONB NOT NULL DEFAULT '{}'::jsonb,
  results JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_by TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
  id TEXT PRIMARY KEY,
  date TEXT NOT NULL,
  description TEXT,
  vendor TEXT,
  amount DOUBLE PRECISION NOT NULL,
  type TEXT NOT NULL DEFAULT 'expense',
  category TEXT,
  category_confidence DOUBLE PRECISION DEFAULT 0,
  categorized_by TEXT DEFAULT 'manual',
  reconciled INTEGER DEFAULT 0,
  source TEXT DEFAULT 'manual',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  account_number TEXT,
  bank_txn_id TEXT,
  qb_txn_id TEXT,
  match_confidence DOUBLE PRECISION DEFAULT 0,
  match_method TEXT,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE reconciliation_log (
  id TEXT PRIMARY KEY,
  period TEXT NOT NULL,
  bank_balance DOUBLE PRECISION,
  qb_balance DOUBLE PRECISION,
  hub_balance DOUBLE PRECISION,
  discrepancy DOUBLE PRECISION DEFAULT 0,
  status TEXT DEFAULT 'pending',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pipeline_deals (
  id TEXT PRIMARY KEY,
  pipeline TEXT NOT NULL,
  contact_id TEXT,
  name TEXT NOT NULL,
  stage TEXT NOT NULL DEFAULT 'prospect',
  amount DOUBLE PRECISION DEFAULT 0,
  probability DOUBLE PRECISION DEFAULT 0,
  owner TEXT,
  last_contact_at TIMESTAMPTZ,
  next_action TEXT,
  next_action_date TEXT,
  stale_days INTEGER DEFAULT 0,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  wire_transaction_id TEXT,
  commitment_date TEXT,
  wire_date TEXT,
  docs_status TEXT DEFAULT 'none',
  investor_email TEXT
);

CREATE TABLE outbound_sequences (
  id TEXT PRIMARY KEY,
  prospect_id TEXT NOT NULL,
  prospect_name TEXT,
  prospect_company TEXT,
  prospect_email TEXT,
  prospect_data JSONB DEFAULT '{}'::jsonb,
  icp_score DOUBLE PRECISION DEFAULT 0,
  sequence_step INTEGER DEFAULT 0,
  status TEXT DEFAULT 'draft',
  last_sent_at TIMESTAMPTZ,
  last_response_at TIMESTAMPTZ,
  engagement_score DOUBLE PRECISION DEFAULT 0,
  qualified INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  content_type TEXT DEFAULT 'email',
  artifact_id TEXT,
  tracked_url TEXT,
  source_agent_id TEXT,
  page_slug TEXT,
  max_scroll INTEGER DEFAULT 0,
  total_seconds INTEGER DEFAULT 0,
  visit_count INTEGER DEFAULT 0,
  forwarded_to TEXT,
  source_sequence_id TEXT,
  source_type TEXT DEFAULT 'general'
);

CREATE TABLE outbound_messages (
  id TEXT PRIMARY KEY,
  sequence_id TEXT NOT NULL,
  step INTEGER NOT NULL,
  channel TEXT DEFAULT 'email',
  subject TEXT,
  body TEXT,
  sent_at TIMESTAMPTZ,
  opened_at TIMESTAMPTZ,
  replied_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sequence_id) REFERENCES outbound_sequences(id)
);

CREATE TABLE communication_queue (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  source_id TEXT,
  from_address TEXT,
  from_name TEXT,
  subject TEXT,
  preview TEXT,
  urgency TEXT DEFAULT 'routine',
  routed_to JSONB DEFAULT '[]'::jsonb,
  classification JSONB DEFAULT '{}'::jsonb,
  processed INTEGER DEFAULT 0,
  processed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  processed_by TEXT,
  source_channel TEXT,
  source_ts TEXT,
  action_taken TEXT
);

CREATE TABLE project_dependencies (
  id TEXT PRIMARY KEY,
  source_initiative_id TEXT NOT NULL,
  target_initiative_id TEXT NOT NULL,
  dependency_type TEXT DEFAULT 'blocks',
  status TEXT DEFAULT 'active',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE automation_coverage (
  id TEXT PRIMARY KEY,
  process_name TEXT NOT NULL,
  description TEXT,
  current_method TEXT DEFAULT 'manual',
  hub_replacement TEXT,
  hub_ready INTEGER DEFAULT 0,
  monthly_cost_manual DOUBLE PRECISION DEFAULT 0,
  monthly_cost_hub DOUBLE PRECISION DEFAULT 0,
  savings_monthly DOUBLE PRECISION DEFAULT 0,
  priority TEXT DEFAULT 'medium',
  assigned_to TEXT,
  status TEXT DEFAULT 'identified',
  activated_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE client_health_scores (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  client_name TEXT,
  health_score INTEGER DEFAULT 50,
  churn_risk INTEGER DEFAULT 0,
  revenue_monthly DOUBLE PRECISION DEFAULT 0,
  revenue_trend TEXT DEFAULT 'stable',
  ar_aging_days INTEGER DEFAULT 0,
  last_comm_days INTEGER DEFAULT 0,
  jockey_conversion_ready INTEGER DEFAULT 0,
  jockey_margin_estimate DOUBLE PRECISION DEFAULT 0,
  signals JSONB DEFAULT '{}'::jsonb,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE training_needs (
  id TEXT PRIMARY KEY,
  person_email TEXT NOT NULL,
  skill_name TEXT NOT NULL,
  current_level TEXT DEFAULT 'none',
  target_level TEXT DEFAULT 'proficient',
  priority TEXT DEFAULT 'medium',
  status TEXT DEFAULT 'identified',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMPTZ
);

CREATE TABLE storefront_leads (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  company TEXT,
  project_description TEXT,
  timeline TEXT,
  budget_range TEXT,
  status TEXT DEFAULT 'new',
  assigned_to TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE client_jockey_configs (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  project_name TEXT,
  tech_stack JSONB DEFAULT '{}'::jsonb,
  conventions TEXT,
  deploy_target TEXT,
  repo_url TEXT,
  total_sessions_planned INTEGER DEFAULT 0,
  total_sessions_completed INTEGER DEFAULT 0,
  total_cost_usd DOUBLE PRECISION DEFAULT 0,
  revenue_monthly DOUBLE PRECISION DEFAULT 0,
  margin_actual DOUBLE PRECISION DEFAULT 0,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content_library (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  content_type TEXT NOT NULL,
  body TEXT,
  status TEXT DEFAULT 'draft',
  target_audience TEXT,
  channel TEXT,
  created_by TEXT DEFAULT 'agent',
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE deck_templates (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  deck_type TEXT NOT NULL,
  slide_structure JSONB NOT NULL DEFAULT '[]'::jsonb,
  data_sources JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_patterns (
  id TEXT PRIMARY KEY,
  pattern_type TEXT NOT NULL,
  source_agent TEXT,
  description TEXT NOT NULL,
  frequency INTEGER DEFAULT 1,
  impact TEXT,
  suggestion TEXT,
  applied INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE call_transcripts (
  id TEXT PRIMARY KEY,
  calendar_event_id TEXT,
  call_type TEXT DEFAULT 'general',
  participants JSONB DEFAULT '[]'::jsonb,
  transcript TEXT,
  summary TEXT,
  action_items JSONB DEFAULT '[]'::jsonb,
  follow_ups JSONB DEFAULT '[]'::jsonb,
  sentiment TEXT,
  coaching_notes JSONB DEFAULT '[]'::jsonb,
  duration_seconds INTEGER DEFAULT 0,
  recorded_at TIMESTAMPTZ,
  processed INTEGER DEFAULT 0,
  processed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE call_templates (
  id TEXT PRIMARY KEY,
  call_type TEXT NOT NULL UNIQUE,
  pre_call_prompt TEXT NOT NULL,
  coaching_prompt TEXT NOT NULL,
  post_call_prompt TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hub_events (
  id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  actor_type TEXT NOT NULL,
  actor_id TEXT NOT NULL,
  entity_type TEXT,
  entity_id TEXT,
  detail TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE investor_profiles (
  id TEXT PRIMARY KEY,
  name TEXT,
  email TEXT,
  entity_name TEXT,
  amount_committed INTEGER,
  amount_funded INTEGER,
  status TEXT,
  tranche INTEGER,
  docs_signed INTEGER,
  date_funded TEXT,
  address TEXT,
  notes TEXT,
  share_token TEXT,
  last_view_at TIMESTAMPTZ,
  view_count INTEGER DEFAULT 0
);

CREATE TABLE sm_tools (
  id TEXT PRIMARY KEY,
  vendor TEXT,
  department TEXT,
  monthly_cost DOUBLE PRECISION,
  hub_replaces INTEGER,
  status TEXT,
  notes TEXT
);

CREATE TABLE partner_commitments (
  id BIGSERIAL PRIMARY KEY,
  partner_email TEXT NOT NULL,
  commitment TEXT NOT NULL,
  source TEXT,
  due_date TEXT,
  status TEXT DEFAULT 'open',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  resolved_at TIMESTAMPTZ,
  nudge_count INTEGER DEFAULT 0
);

CREATE TABLE brief_pins (
  id BIGSERIAL PRIMARY KEY,
  item_id TEXT NOT NULL,
  item_type TEXT NOT NULL,
  user_email TEXT NOT NULL,
  title TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(item_id, user_email)
);

CREATE TABLE rate_limits (
  key TEXT PRIMARY KEY,
  count INTEGER NOT NULL DEFAULT 1,
  window_start TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hub_feedback (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL DEFAULT 'feedback',
  agent_id TEXT,
  run_id TEXT,
  user_email TEXT NOT NULL DEFAULT 'aaron@sprintmode.co',
  content TEXT,
  agent_response TEXT,
  data_context TEXT,
  status TEXT NOT NULL DEFAULT 'new',
  resolved_by TEXT,
  resolved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE connector_sync_log (
  id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  status TEXT DEFAULT 'success',
  details TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE chart_of_accounts (
  id TEXT PRIMARY KEY,
  account_number TEXT NOT NULL,
  account_name TEXT NOT NULL,
  account_type TEXT NOT NULL,
  hub_category TEXT,
  parent_account_id TEXT,
  description TEXT,
  is_active INTEGER DEFAULT 1,
  source TEXT DEFAULT 'plotpath',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE bank_transactions (
  id TEXT PRIMARY KEY,
  plaid_transaction_id TEXT,
  account_id TEXT,
  date TEXT NOT NULL,
  amount DOUBLE PRECISION NOT NULL,
  name TEXT,
  merchant_name TEXT,
  category TEXT,
  hub_category TEXT,
  hub_category_confidence DOUBLE PRECISION DEFAULT 0,
  pending INTEGER DEFAULT 0,
  matched_qb_txn_id TEXT,
  matched_hub_txn_id TEXT,
  match_confidence DOUBLE PRECISION DEFAULT 0,
  match_method TEXT,
  reviewed_by TEXT,
  reviewed_at TIMESTAMPTZ,
  source TEXT DEFAULT 'plaid',
  raw_json JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE reconciliation_tasks (
  id TEXT PRIMARY KEY,
  period TEXT NOT NULL,
  task_type TEXT NOT NULL,
  description TEXT NOT NULL,
  bank_txn_id TEXT,
  qb_txn_id TEXT,
  hub_txn_id TEXT,
  amount DOUBLE PRECISION,
  suggested_action TEXT,
  status TEXT DEFAULT 'open',
  resolved_by TEXT,
  resolved_at TIMESTAMPTZ,
  resolution_notes TEXT,
  priority INTEGER DEFAULT 5,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  assigned_to TEXT,
  escalated_by TEXT,
  escalated_at TIMESTAMPTZ,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE monthly_close (
  id TEXT PRIMARY KEY,
  period TEXT NOT NULL,
  step_name TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  completed_by TEXT,
  completed_at TIMESTAMPTZ,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE agent_kpis (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  period TEXT NOT NULL,
  total_runs INTEGER DEFAULT 0,
  successful_runs INTEGER DEFAULT 0,
  approval_rate DOUBLE PRECISION,
  avg_response_time_ms INTEGER,
  user_edits INTEGER DEFAULT 0,
  rejections INTEGER DEFAULT 0,
  escalations INTEGER DEFAULT 0,
  hallucination_flags INTEGER DEFAULT 0,
  tokens_used INTEGER DEFAULT 0,
  cost_usd DOUBLE PRECISION DEFAULT 0,
  autonomy_level_avg DOUBLE PRECISION,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  UNIQUE(agent_id, period)
);

CREATE TABLE agent_role_templates (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  description TEXT,
  sidebar_items JSONB NOT NULL,
  brief_agents JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stripe_transactions (
  id TEXT PRIMARY KEY,
  charge_id TEXT UNIQUE,
  date TEXT NOT NULL,
  amount DOUBLE PRECISION NOT NULL,
  description TEXT,
  customer_id TEXT,
  status TEXT,
  matched_invoice_id TEXT,
  raw_json JSONB,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE ramp_transactions (
  id TEXT PRIMARY KEY,
  ramp_id TEXT UNIQUE,
  date TEXT NOT NULL,
  amount DOUBLE PRECISION NOT NULL,
  merchant_name TEXT,
  category TEXT,
  user_name TEXT,
  card_name TEXT,
  raw_json JSONB,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  hub_category TEXT,
  hub_category_confidence DOUBLE PRECISION DEFAULT 0,
  description TEXT
);

CREATE TABLE vendor_rules (
  id TEXT PRIMARY KEY,
  vendor_pattern TEXT NOT NULL,
  hub_category TEXT NOT NULL,
  account_number TEXT,
  confidence DOUBLE PRECISION DEFAULT 0.90,
  created_by TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE tool_inventory (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  monthly_cost DOUBLE PRECISION DEFAULT 0,
  owner_email TEXT,
  division TEXT,
  status TEXT DEFAULT 'active',
  hub_replacement TEXT,
  has_api INTEGER DEFAULT 0,
  api_connected INTEGER DEFAULT 0,
  connection_status TEXT DEFAULT 'not_connected',
  last_charge_date TEXT,
  charge_count INTEGER DEFAULT 0,
  total_spend DOUBLE PRECISION DEFAULT 0,
  notes TEXT,
  decision TEXT,
  decided_by TEXT,
  decided_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  replacement_status TEXT DEFAULT 'not_started',
  replacement_notes TEXT,
  dependencies_json JSONB DEFAULT '[]'::jsonb,
  savings_to_date DOUBLE PRECISION DEFAULT 0,
  cancel_date TEXT,
  source TEXT DEFAULT 'manual',
  category TEXT,
  hub_replacement_agent TEXT,
  vendor TEXT,
  hours_automated DOUBLE PRECISION DEFAULT 0
);

CREATE TABLE narrative_versions (
  id TEXT PRIMARY KEY,
  variant TEXT NOT NULL,
  audience TEXT NOT NULL,
  title TEXT,
  body TEXT,
  version INTEGER DEFAULT 1,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  doc_type TEXT DEFAULT 'pitch',
  owner TEXT DEFAULT 'aaron',
  stale_reason TEXT,
  last_verified_at TIMESTAMPTZ
);

CREATE TABLE narrative_contexts (
  id TEXT PRIMARY KEY,
  entity TEXT NOT NULL,
  status TEXT,
  positioning TEXT,
  key_facts TEXT,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE cracked_findings (
  id TEXT PRIMARY KEY,
  category TEXT,
  title TEXT NOT NULL,
  description TEXT,
  cost_benefit TEXT,
  impact_score DOUBLE PRECISION DEFAULT 0,
  auto_eligible INTEGER DEFAULT 0,
  status TEXT DEFAULT 'new',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE cracked_proposals (
  id TEXT PRIMARY KEY,
  finding_id TEXT,
  proposal_type TEXT,
  target_agent_id TEXT,
  change_description TEXT,
  risk_level TEXT DEFAULT 'medium',
  status TEXT DEFAULT 'pending',
  applied_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE security_controls (
  id TEXT PRIMARY KEY,
  category TEXT NOT NULL,
  control_name TEXT NOT NULL,
  status TEXT DEFAULT 'not_started',
  evidence TEXT,
  last_verified TEXT,
  responsible TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE connector_registry (
  id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  connector_type TEXT,
  status TEXT DEFAULT 'active',
  data_scope TEXT,
  health_score DOUBLE PRECISION DEFAULT 1.0,
  last_sync TEXT,
  lifecycle_stage TEXT DEFAULT 'read',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE company_profiles (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  industry TEXT,
  team_size INTEGER,
  revenue TEXT,
  challenges TEXT,
  agent_roster TEXT,
  transformation_plan TEXT,
  logo_url TEXT,
  accent_color TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  conversation_policy TEXT DEFAULT 'balanced'
);

CREATE TABLE onboarding_sessions (
  id TEXT PRIMARY KEY,
  company_id TEXT,
  step INTEGER DEFAULT 1,
  data TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clone_profiles (
  id TEXT PRIMARY KEY,
  tenant_id TEXT DEFAULT 'sprint_mode',
  user_email TEXT NOT NULL,
  clone_name TEXT,
  operating_manual TEXT,
  decision_frameworks TEXT,
  communication_style TEXT,
  priorities TEXT,
  quality_bar TEXT,
  blind_spots TEXT,
  strengths TEXT,
  common_phrases TEXT,
  status TEXT DEFAULT 'training',
  training_progress DOUBLE PRECISION DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clone_training_signals (
  id TEXT PRIMARY KEY,
  clone_id TEXT,
  signal_type TEXT,
  source TEXT,
  context TEXT,
  decision_made TEXT,
  outcome TEXT,
  confidence DOUBLE PRECISION DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clone_decisions (
  id TEXT PRIMARY KEY,
  clone_id TEXT,
  scenario_id TEXT,
  clone_decision TEXT,
  human_decision TEXT,
  agreement INTEGER,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clone_scenarios (
  id TEXT PRIMARY KEY,
  tenant_id TEXT DEFAULT 'sprint_mode',
  title TEXT,
  context TEXT,
  expected_decision TEXT,
  category TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE blended_clones (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  clone_weights TEXT,
  purpose TEXT,
  active INTEGER DEFAULT 1,
  tenant_id TEXT DEFAULT 'sprint_mode',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vault_items (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  owner TEXT NOT NULL,
  category TEXT NOT NULL,
  label TEXT NOT NULL,
  has_secondary INTEGER DEFAULT 0,
  secondary_label TEXT,
  expires_at TIMESTAMPTZ,
  renewal_url TEXT,
  renewal_lead_days INTEGER DEFAULT 90,
  notes TEXT,
  last_accessed_at TIMESTAMPTZ,
  access_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  shared INTEGER DEFAULT 0
);

CREATE TABLE vault_access_log (
  id TEXT PRIMARY KEY,
  vault_item_id TEXT NOT NULL,
  accessed_by TEXT NOT NULL,
  action TEXT NOT NULL,
  ip_address TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vault_auth_tokens (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  token TEXT NOT NULL UNIQUE,
  expires_at TIMESTAMPTZ NOT NULL,
  used INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_conversations (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  title TEXT DEFAULT 'New conversation',
  visibility TEXT DEFAULT 'shared',
  last_message_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  message_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sharing_config (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  target_hub_url TEXT NOT NULL,
  target_hub_name TEXT,
  fields_shared TEXT DEFAULT '["cash","health_score","revenue","agent_count","critical_count"]',
  secret TEXT,
  granted_by TEXT,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hub_external_data (
  id TEXT PRIMARY KEY,
  source_hub_url TEXT NOT NULL,
  source_hub_name TEXT,
  field TEXT NOT NULL,
  value TEXT,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_tool_audit (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_id TEXT NOT NULL,
  user_email TEXT,
  tool_type TEXT NOT NULL,
  tool_name TEXT,
  input_summary TEXT,
  result_summary TEXT,
  autonomy_level INTEGER,
  approved_by TEXT,
  blocked_by TEXT,
  cost_usd DOUBLE PRECISION DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_scopes (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_id TEXT NOT NULL,
  client_email TEXT,
  client_name TEXT,
  description TEXT NOT NULL,
  scope_doc TEXT,
  pricing_estimate DOUBLE PRECISION,
  status TEXT DEFAULT 'draft',
  files_json JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_projects (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  scope_id TEXT NOT NULL,
  agent_id TEXT NOT NULL,
  client_email TEXT,
  client_name TEXT,
  status TEXT DEFAULT 'pending_payment',
  tier TEXT DEFAULT 'prototype',
  total_price DOUBLE PRECISION DEFAULT 0,
  deposit_paid DOUBLE PRECISION DEFAULT 0,
  stripe_payment_id TEXT,
  delivery_target TEXT,
  phases_json JSONB DEFAULT '[]'::jsonb,
  acceptance_status TEXT DEFAULT 'pending',
  acceptance_deadline TEXT,
  revision_count INTEGER DEFAULT 0,
  max_revisions INTEGER DEFAULT 2,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  client_access_token TEXT
);

CREATE TABLE storefront_deliverables (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  filename TEXT NOT NULL,
  file_type TEXT,
  file_url TEXT,
  size_bytes INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_api_keys (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  key_hash TEXT NOT NULL,
  label TEXT,
  scopes JSONB DEFAULT '["scope","project","deliverables"]'::jsonb,
  rate_limit INTEGER DEFAULT 100,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE privacy_subscribers (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  email TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  plan TEXT DEFAULT 'free',
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  pii_json JSONB DEFAULT '{}'::jsonb,
  scan_status TEXT DEFAULT 'idle',
  last_scan_at TIMESTAMPTZ,
  broker_count INTEGER DEFAULT 0,
  removed_count INTEGER DEFAULT 0,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE privacy_scans (
  id TEXT PRIMARY KEY,
  subscriber_id TEXT NOT NULL,
  status TEXT DEFAULT 'queued',
  scan_type TEXT DEFAULT 'full',
  brokers_checked INTEGER DEFAULT 0,
  brokers_found INTEGER DEFAULT 0,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  results_json JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE privacy_removals (
  id TEXT PRIMARY KEY,
  subscriber_id TEXT NOT NULL,
  scan_id TEXT,
  broker_name TEXT NOT NULL,
  broker_url TEXT,
  status TEXT DEFAULT 'pending',
  method TEXT DEFAULT 'auto',
  submitted_at TIMESTAMPTZ,
  verified_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE privacy_brokers (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  domain TEXT NOT NULL,
  opt_out_url TEXT,
  scan_enabled INTEGER DEFAULT 1,
  removal_enabled INTEGER DEFAULT 1,
  category TEXT DEFAULT 'people_search',
  difficulty TEXT DEFAULT 'easy',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_brands (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_id TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  domain TEXT,
  tagline TEXT,
  description TEXT,
  accent_color TEXT DEFAULT '#4F6EF7',
  bg_color TEXT DEFAULT '#FAFBFC',
  logo_text TEXT,
  pricing_json JSONB DEFAULT '{}'::jsonb,
  scoping_intro TEXT,
  cta_text TEXT DEFAULT 'Get Started',
  features_json JSONB DEFAULT '[]'::jsonb,
  legal_entity TEXT,
  stripe_price_id TEXT,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  stripe_account_id TEXT,
  connect_status TEXT DEFAULT 'none',
  connect_onboarded_at TIMESTAMPTZ
);

CREATE TABLE storefront_gtm_configs (
  id TEXT PRIMARY KEY,
  brand_slug TEXT NOT NULL,
  agent_id TEXT DEFAULT 'agent_gtm',
  icp_json JSONB NOT NULL,
  channels_json JSONB DEFAULT '[]'::jsonb,
  messaging_json JSONB DEFAULT '{}'::jsonb,
  kpis_json JSONB DEFAULT '{}'::jsonb,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_outbound_sequences (
  id TEXT PRIMARY KEY,
  brand_slug TEXT NOT NULL,
  sequence_name TEXT NOT NULL,
  steps_json JSONB NOT NULL,
  target_persona TEXT,
  tone TEXT DEFAULT 'professional',
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_evaluations (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  evaluation_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  viability_score DOUBLE PRECISION DEFAULT 0,
  automation_pct INTEGER DEFAULT 0,
  margin_estimate DOUBLE PRECISION DEFAULT 0,
  acquisition_score DOUBLE PRECISION DEFAULT 0,
  market_size TEXT,
  competition TEXT,
  pricing_model TEXT,
  target_buyer TEXT,
  strengths_json JSONB DEFAULT '[]'::jsonb,
  risks_json JSONB DEFAULT '[]'::jsonb,
  recommendation TEXT,
  status TEXT DEFAULT 'evaluated',
  approved INTEGER DEFAULT 0,
  approved_at TIMESTAMPTZ,
  prd_generated INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_metrics_daily (
  id TEXT PRIMARY KEY,
  brand_slug TEXT NOT NULL,
  date TEXT NOT NULL,
  visits INTEGER DEFAULT 0,
  signups INTEGER DEFAULT 0,
  scans_started INTEGER DEFAULT 0,
  scans_completed INTEGER DEFAULT 0,
  subscriptions INTEGER DEFAULT 0,
  revenue_cents INTEGER DEFAULT 0,
  churn INTEGER DEFAULT 0,
  outbound_sent INTEGER DEFAULT 0,
  outbound_opens INTEGER DEFAULT 0,
  outbound_replies INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_experiments (
  id TEXT PRIMARY KEY,
  brand_slug TEXT NOT NULL,
  experiment_type TEXT NOT NULL,
  variant_a TEXT NOT NULL,
  variant_b TEXT NOT NULL,
  metric TEXT NOT NULL,
  start_date TEXT,
  end_date TEXT,
  result_a DOUBLE PRECISION,
  result_b DOUBLE PRECISION,
  winner TEXT,
  status TEXT DEFAULT 'running',
  created_by TEXT DEFAULT 'agent_growth',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE saas_subscriptions (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  tool_name TEXT NOT NULL,
  vendor TEXT,
  monthly_cost DOUBLE PRECISION DEFAULT 0,
  annual_cost DOUBLE PRECISION DEFAULT 0,
  category TEXT,
  hub_replacement_agent TEXT,
  replacement_status TEXT DEFAULT 'not_started',
  replacement_notes TEXT,
  dependencies_json JSONB DEFAULT '[]'::jsonb,
  data_migrated INTEGER DEFAULT 0,
  cancel_date TEXT,
  savings_to_date DOUBLE PRECISION DEFAULT 0,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_prds (
  id TEXT PRIMARY KEY,
  evaluation_id TEXT,
  agent_id TEXT NOT NULL,
  brand_name TEXT NOT NULL,
  brand_slug TEXT,
  prd_json JSONB NOT NULL,
  session_chain_json JSONB DEFAULT '[]'::jsonb,
  status TEXT DEFAULT 'draft',
  approved INTEGER DEFAULT 0,
  approved_at TIMESTAMPTZ,
  jockey_project_id TEXT,
  sessions_total INTEGER DEFAULT 0,
  sessions_completed INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_transactions (
  id TEXT PRIMARY KEY,
  source_hub_id TEXT,
  source_agent_id TEXT,
  target_storefront TEXT NOT NULL,
  tool_name TEXT NOT NULL,
  request_json JSONB,
  response_json JSONB,
  status TEXT DEFAULT 'pending',
  latency_ms INTEGER,
  revenue_cents INTEGER DEFAULT 0,
  platform_fee_cents INTEGER DEFAULT 0,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evolver_audits (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  status TEXT NOT NULL,
  findings TEXT,
  recommended_prompt TEXT,
  recommended_action TEXT,
  severity TEXT DEFAULT 'low',
  applied INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evolver_runs (
  id TEXT PRIMARY KEY,
  agents_audited INTEGER,
  stale_count INTEGER,
  dormant_count INTEGER,
  missing_count INTEGER,
  current_count INTEGER,
  summary TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE narrative_signals (
  id TEXT PRIMARY KEY,
  source_agent TEXT NOT NULL,
  signal_type TEXT NOT NULL,
  entity TEXT,
  summary TEXT,
  processed INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  data_json JSONB
);

CREATE TABLE narrative_pushes (
  id TEXT PRIMARY KEY,
  narrative_version_id TEXT NOT NULL,
  target_agent TEXT NOT NULL,
  pushed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  acknowledged INTEGER DEFAULT 0
);

CREATE TABLE narrative_faqs (
  id TEXT PRIMARY KEY,
  entity TEXT NOT NULL,
  audience TEXT NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  source TEXT,
  verified INTEGER DEFAULT 0,
  verified_at TIMESTAMPTZ,
  pushed_to_json JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE narrative_threads (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  title TEXT NOT NULL,
  entity TEXT,
  audience TEXT,
  messages_json JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ingestion_previews (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  filename TEXT,
  file_type TEXT,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','applied','rejected')),
  proposed_changes TEXT NOT NULL,
  summary TEXT,
  row_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  applied_at TIMESTAMPTZ,
  applied_by TEXT
);

CREATE TABLE agent_actions (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  action_type TEXT NOT NULL,
  target_table TEXT NOT NULL,
  target_id TEXT,
  operation TEXT NOT NULL CHECK (operation IN ('insert','update','delete')),
  sql_statement TEXT NOT NULL,
  description TEXT NOT NULL,
  autonomy_level INTEGER NOT NULL DEFAULT 1,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','executed','rejected','failed')),
  approved_by TEXT,
  executed_at TIMESTAMPTZ,
  error_detail TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  prompt_text TEXT
);

CREATE TABLE hub_knowledge (
  id TEXT PRIMARY KEY,
  filename TEXT NOT NULL,
  content TEXT NOT NULL,
  category TEXT NOT NULL DEFAULT 'brain',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  section_slug TEXT,
  assigned_to TEXT,
  entry_type TEXT DEFAULT 'current_state',
  searchable_keywords TEXT,
  tenant_id TEXT DEFAULT 'sprint_mode',
  access_tier INTEGER DEFAULT 0,
  knowledge_domain TEXT DEFAULT 'global',
  title TEXT DEFAULT '',
  source TEXT DEFAULT 'repo_sync',
  created_at TIMESTAMPTZ DEFAULT '2026-03-23'
);

CREATE TABLE agent_work_queue (
  id TEXT PRIMARY KEY,
  tenant_id TEXT DEFAULT 'sprint_mode',
  agent_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  payload JSONB DEFAULT '{}'::jsonb,
  status TEXT DEFAULT 'pending',
  result TEXT,
  error TEXT,
  priority INTEGER DEFAULT 5,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  cost_usd DOUBLE PRECISION DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_agent_permissions (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  agent_id TEXT NOT NULL,
  can_view INTEGER DEFAULT 1,
  can_chat INTEGER DEFAULT 1,
  can_approve INTEGER DEFAULT 0,
  can_see_financials INTEGER DEFAULT 0,
  can_configure INTEGER DEFAULT 0,
  can_execute INTEGER DEFAULT 0,
  set_by TEXT DEFAULT 'system',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ,
  tone TEXT DEFAULT 'balanced',
  language TEXT DEFAULT 'en',
  UNIQUE(user_email, agent_id)
);

CREATE TABLE role_templates (
  id TEXT PRIMARY KEY,
  role_name TEXT NOT NULL,
  description TEXT,
  agent_permissions TEXT NOT NULL,
  sidebar_default TEXT,
  brief_agents JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE company_type_templates (
  id TEXT PRIMARY KEY,
  type_name TEXT NOT NULL,
  description TEXT,
  default_agents TEXT NOT NULL,
  default_sidebar TEXT NOT NULL,
  onboarding_questions JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE brief_cache (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  tenant_id TEXT DEFAULT 'sprint_mode',
  sections_json JSONB NOT NULL,
  strip_json JSONB,
  generated_at TIMESTAMPTZ NOT NULL,
  expires_at TIMESTAMPTZ,
  UNIQUE(user_email, tenant_id)
);

CREATE TABLE storefront_products (
  id TEXT PRIMARY KEY,
  brand_slug TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  price_cents INTEGER NOT NULL,
  interval TEXT DEFAULT 'month',
  stripe_price_id TEXT,
  stripe_product_id TEXT,
  active INTEGER DEFAULT 1,
  features JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_customers (
  id TEXT PRIMARY KEY,
  brand_slug TEXT NOT NULL,
  email TEXT NOT NULL,
  name TEXT,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  product_id TEXT,
  status TEXT DEFAULT 'active',
  mrr_cents INTEGER DEFAULT 0,
  provisioned_at TIMESTAMPTZ,
  cancelled_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  source TEXT DEFAULT 'human',
  UNIQUE(brand_slug, email)
);

CREATE TABLE client_migrations (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  client_name TEXT NOT NULL,
  current_revenue INTEGER DEFAULT 0,
  current_margin_pct DOUBLE PRECISION DEFAULT 50,
  projected_margin_pct DOUBLE PRECISION DEFAULT 95,
  status TEXT DEFAULT 'evaluation',
  readiness_score DOUBLE PRECISION DEFAULT 0,
  complexity TEXT DEFAULT 'medium',
  tech_stack JSONB DEFAULT '[]'::jsonb,
  sessions_planned INTEGER DEFAULT 0,
  sessions_completed INTEGER DEFAULT 0,
  total_cost_usd DOUBLE PRECISION DEFAULT 0,
  savings_monthly DOUBLE PRECISION DEFAULT 0,
  approved_by TEXT,
  approved_at TIMESTAMPTZ,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ
);

CREATE TABLE hub_subscriptions (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  plan TEXT NOT NULL DEFAULT 'start',
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  status TEXT DEFAULT 'trialing',
  mrr_cents INTEGER DEFAULT 0,
  trial_ends_at TIMESTAMPTZ,
  billing_email TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ,
  billing_cycle TEXT DEFAULT 'monthly',
  current_period_end TEXT,
  UNIQUE(tenant_id)
);

CREATE TABLE tenant_invites (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  email TEXT NOT NULL,
  role TEXT DEFAULT 'team',
  invited_by TEXT,
  accepted_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(tenant_id, email)
);

CREATE TABLE user_tenants (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  tenant_id TEXT NOT NULL,
  role TEXT DEFAULT 'team',
  is_owner INTEGER DEFAULT 0,
  is_admin INTEGER DEFAULT 0,
  joined_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  access_tier INTEGER DEFAULT 1,
  ui_mode TEXT DEFAULT 'standard',
  UNIQUE(user_email, tenant_id)
);

CREATE TABLE action_audit (
  id TEXT PRIMARY KEY,
  card_id TEXT,
  agent_id TEXT,
  action_type TEXT,
  action_label TEXT,
  user_email TEXT,
  status TEXT DEFAULT 'pending',
  result TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMPTZ,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE card_snooze (
  id TEXT PRIMARY KEY,
  card_id TEXT,
  user_email TEXT,
  snooze_until TIMESTAMPTZ,
  dismissed INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bug_reports (
  id TEXT PRIMARY KEY,
  user_email TEXT,
  page TEXT,
  description TEXT,
  status TEXT DEFAULT 'open',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE jockey_usage_log (
  id TEXT PRIMARY KEY,
  session_id TEXT,
  tenant_id TEXT,
  usage_type TEXT DEFAULT 'internal',
  cost_usd DOUBLE PRECISION DEFAULT 0,
  created_at TIMESTAMPTZ
);

CREATE TABLE jockey_runner_config (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  runner_type TEXT DEFAULT 'shared',
  repo_url TEXT,
  github_app_installation_id TEXT,
  deploy_target TEXT DEFAULT 'cloudflare',
  max_concurrent INTEGER DEFAULT 2,
  monthly_session_limit INTEGER DEFAULT 50,
  monthly_cost_limit_usd DOUBLE PRECISION DEFAULT 100,
  api_key_source TEXT DEFAULT 'platform',
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
);

CREATE TABLE agent_model_usage (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  agent_name TEXT,
  model TEXT NOT NULL,
  tokens_in INTEGER DEFAULT 0,
  tokens_out INTEGER DEFAULT 0,
  cache_read_tokens INTEGER DEFAULT 0,
  cache_write_tokens INTEGER DEFAULT 0,
  latency_ms INTEGER DEFAULT 0,
  cost_cents DOUBLE PRECISION DEFAULT 0,
  success INTEGER DEFAULT 1,
  error_message TEXT,
  trigger TEXT,
  user_email TEXT,
  tenant_id TEXT DEFAULT 'sprint_mode',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  provider TEXT DEFAULT 'anthropic'
);

CREATE TABLE team_analytics (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  period TEXT NOT NULL,
  automation_pct DOUBLE PRECISION DEFAULT 0,
  hub_sessions INTEGER DEFAULT 0,
  hub_minutes DOUBLE PRECISION DEFAULT 0,
  slack_messages INTEGER DEFAULT 0,
  gmail_sent INTEGER DEFAULT 0,
  gmail_received INTEGER DEFAULT 0,
  jira_updates INTEGER DEFAULT 0,
  deel_hours DOUBLE PRECISION DEFAULT 0,
  top_agents TEXT,
  focus_areas TEXT,
  struggle_signals TEXT,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ,
  UNIQUE(user_email, period)
);

CREATE TABLE legal_matters (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  matter_type TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'open',
  priority TEXT DEFAULT 'medium',
  owner TEXT,
  counsel TEXT,
  deadline TEXT,
  decided_date TEXT,
  decided_by TEXT,
  decision_summary TEXT,
  source TEXT,
  related_entity TEXT,
  related_matter_id TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sender_reputation (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  sender TEXT NOT NULL,
  source TEXT NOT NULL DEFAULT 'email',
  classification TEXT NOT NULL DEFAULT 'unknown',
  confidence DOUBLE PRECISION DEFAULT 0.5,
  total_messages INTEGER DEFAULT 0,
  routed_count INTEGER DEFAULT 0,
  filed_count INTEGER DEFAULT 0,
  dismissed_count INTEGER DEFAULT 0,
  user_overrides INTEGER DEFAULT 0,
  last_message_at TIMESTAMPTZ,
  last_classification TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_classifications (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  email_id TEXT,
  from_addr TEXT,
  subject TEXT,
  classification TEXT NOT NULL,
  confidence DOUBLE PRECISION DEFAULT 0.5,
  signals_json JSONB,
  user_override TEXT,
  overridden_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE outbound_slack_messages (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  channel TEXT NOT NULL,
  channel_name TEXT,
  text TEXT NOT NULL,
  thread_ts TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  approved_by TEXT,
  approved_at TIMESTAMPTZ,
  sent_at TIMESTAMPTZ,
  message_ts TEXT,
  agent_id TEXT,
  run_id TEXT,
  triggered_by TEXT,
  error TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shared_threads (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  conversation_id TEXT NOT NULL,
  agent_id TEXT,
  shared_by TEXT NOT NULL,
  shared_with TEXT NOT NULL,
  message_id TEXT,
  note TEXT,
  status TEXT DEFAULT 'unread',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tour_guide_progress (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  user_email TEXT NOT NULL,
  step_type TEXT NOT NULL,
  step_id TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  completed_at TIMESTAMPTZ,
  dismissed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE page_tips (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  user_email TEXT NOT NULL,
  page_id TEXT NOT NULL,
  tip_text TEXT NOT NULL,
  capabilities_json JSONB,
  dismissed INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE feature_announcements (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  feature_key TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  relevant_roles TEXT,
  action_label TEXT,
  action_url TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE feature_announcement_views (
  id TEXT PRIMARY KEY,
  announcement_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  shown_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  dismissed_at TIMESTAMPTZ
);

CREATE TABLE user_feature_usage (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  user_email TEXT NOT NULL,
  feature_key TEXT NOT NULL,
  first_used_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  use_count INTEGER DEFAULT 1,
  last_used_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ic_votes (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  deal_id TEXT NOT NULL,
  voter_email TEXT NOT NULL,
  vote TEXT NOT NULL,
  rationale TEXT,
  conditions TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ic_meetings (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  date TEXT NOT NULL,
  attendees TEXT,
  agenda TEXT,
  minutes TEXT,
  deals_reviewed TEXT,
  status TEXT DEFAULT 'scheduled',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_artifacts (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  title TEXT NOT NULL,
  artifact_type TEXT NOT NULL,
  content_html TEXT,
  content_markdown TEXT,
  template TEXT,
  file_url TEXT,
  run_id TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  brief_type TEXT,
  assigned_to TEXT,
  assigned_by TEXT,
  presenting_agent_id TEXT,
  read_at TIMESTAMPTZ,
  shared_thread_id TEXT,
  published_url TEXT,
  published_at TIMESTAMPTZ,
  publish_target TEXT,
  publish_slug TEXT,
  publish_status TEXT DEFAULT 'draft',
  media_type TEXT DEFAULT 'markdown',
  source_file TEXT,
  contact_id TEXT,
  company_id TEXT
);

CREATE TABLE agent_trigger_chains (
  id TEXT PRIMARY KEY,
  source_agent TEXT NOT NULL,
  trigger_event TEXT NOT NULL,
  target_agent TEXT NOT NULL,
  target_trigger TEXT DEFAULT 'a2a_trigger',
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hub_relays (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  from_email TEXT NOT NULL,
  to_email TEXT NOT NULL,
  subject TEXT NOT NULL,
  context TEXT,
  source_agent_id TEXT,
  source_conversation_id TEXT,
  source_run_id TEXT,
  response_conversation_id TEXT,
  status TEXT DEFAULT 'pending',
  priority TEXT DEFAULT 'normal',
  responded_at TIMESTAMPTZ,
  response_text TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  relay_type TEXT DEFAULT 'task',
  thread_id TEXT
);

CREATE TABLE email_threads (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  gmail_thread_id TEXT NOT NULL,
  subject TEXT,
  participants JSONB,
  last_message_at TIMESTAMPTZ,
  message_count INTEGER DEFAULT 1,
  status TEXT DEFAULT 'active',
  assigned_agent TEXT,
  assigned_user TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE deel_contractors (
  id TEXT PRIMARY KEY,
  name TEXT,
  email TEXT,
  country TEXT,
  currency TEXT DEFAULT 'USD',
  contract_type TEXT DEFAULT 'contractor',
  status TEXT DEFAULT 'active',
  monthly_amount DOUBLE PRECISION DEFAULT 0,
  start_date TEXT,
  end_date TEXT,
  job_title TEXT,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE deel_invoices (
  id TEXT PRIMARY KEY,
  contractor_id TEXT,
  amount DOUBLE PRECISION DEFAULT 0,
  currency TEXT DEFAULT 'USD',
  status TEXT DEFAULT 'pending',
  period_start TEXT,
  period_end TEXT,
  paid_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE voice_intakes (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  user_email TEXT NOT NULL,
  transcript TEXT NOT NULL,
  intent TEXT NOT NULL DEFAULT 'note',
  routed_to JSONB,
  target_person TEXT,
  target_entity TEXT,
  confirmation TEXT,
  status TEXT DEFAULT 'processed',
  result_id TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_proposals (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  type TEXT NOT NULL DEFAULT 'feature_request',
  title TEXT NOT NULL,
  description TEXT,
  proposed_by TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending_review' CHECK(status IN ('pending_review','approved','rejected','built')),
  source_conversation_id TEXT,
  reviewed_by TEXT,
  reviewed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE platform_policies (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'platform',
  policy_type TEXT NOT NULL,
  version TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  effective_date TEXT,
  status TEXT DEFAULT 'active',
  created_by TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE platform_violations (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  violation_type TEXT NOT NULL,
  severity TEXT NOT NULL DEFAULT 'warning',
  description TEXT NOT NULL,
  evidence TEXT,
  policy_reference TEXT,
  status TEXT DEFAULT 'open',
  resolution TEXT,
  resolved_by TEXT,
  resolved_at TIMESTAMPTZ,
  created_by TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_suspensions (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_id TEXT NOT NULL,
  reason TEXT NOT NULL,
  violation_id TEXT,
  suspended_by TEXT NOT NULL,
  suspended_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  reinstated_by TEXT,
  reinstated_at TIMESTAMPTZ,
  reinstate_notes TEXT,
  probation_until TIMESTAMPTZ,
  status TEXT DEFAULT 'suspended'
);

CREATE TABLE custom_sidebar_sections (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  section_schema TEXT,
  data_sources JSONB,
  created_by TEXT NOT NULL,
  proposal_id TEXT,
  is_shared INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sidebar_section_shares (
  id TEXT PRIMARY KEY,
  section_id TEXT NOT NULL,
  shared_by TEXT NOT NULL,
  shared_with TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  shared_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  responded_at TIMESTAMPTZ
);

CREATE TABLE deployment_guards (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  file_path TEXT NOT NULL,
  guard_type TEXT DEFAULT 'owns',
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE threads (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_id TEXT,
  user_email TEXT NOT NULL,
  participants JSONB,
  title TEXT DEFAULT 'New thread',
  visibility TEXT DEFAULT 'shared',
  thread_type TEXT DEFAULT 'chat',
  last_message_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  message_count INTEGER DEFAULT 0,
  agents_json JSONB DEFAULT '[]'::jsonb,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  cross_hub INTEGER DEFAULT 0
);

CREATE TABLE hub_notifications (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  user_email TEXT NOT NULL,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT,
  link TEXT,
  source_agent_id TEXT,
  read_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_presence (
  user_email TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  last_active_at TIMESTAMPTZ NOT NULL,
  current_agent_id TEXT,
  status TEXT DEFAULT 'active'
);

CREATE TABLE retry_queue (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  prompt TEXT NOT NULL,
  conversation_id TEXT,
  original_error TEXT,
  retry_count INTEGER DEFAULT 0,
  status TEXT DEFAULT 'queued',
  processed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE provider_health (
  provider TEXT PRIMARY KEY,
  status TEXT DEFAULT 'healthy',
  last_check TEXT,
  last_success TEXT,
  last_error TEXT,
  error_rate_1h DOUBLE PRECISION DEFAULT 0,
  latency_p95_ms INTEGER DEFAULT 0,
  consecutive_failures INTEGER DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE page_analytics (
  id TEXT PRIMARY KEY,
  viewer_name TEXT,
  viewer_email TEXT,
  event TEXT NOT NULL,
  page TEXT,
  detail TEXT,
  referrer TEXT,
  user_agent TEXT,
  ip_country TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  internal INTEGER DEFAULT 0
);

CREATE TABLE release_notes (
  id TEXT PRIMARY KEY,
  session_id TEXT,
  title TEXT NOT NULL,
  summary TEXT,
  features JSONB DEFAULT '[]'::jsonb,
  category TEXT DEFAULT 'improvement',
  commit_hash TEXT,
  commit_date TEXT,
  files_changed INTEGER DEFAULT 0,
  chain TEXT,
  author TEXT DEFAULT 'jockey',
  tenant_id TEXT DEFAULT 'sprint_mode',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_accountability_chain (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  chain_id TEXT NOT NULL,
  sequence_number INTEGER NOT NULL,
  agent_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  action_description TEXT,
  input_summary TEXT,
  output_summary TEXT,
  data_tables_accessed TEXT,
  autonomy_level INTEGER,
  delegated_to TEXT,
  delegated_reason TEXT,
  outcome TEXT,
  duration_ms INTEGER,
  tokens_used INTEGER,
  cost_usd DOUBLE PRECISION,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE brief_actions (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  source_type TEXT NOT NULL,
  source_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  assigned_to TEXT,
  due_date TEXT,
  calendar_event_id TEXT,
  task_id TEXT,
  status TEXT DEFAULT 'pending',
  created_by TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crm_companies (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  name TEXT NOT NULL,
  domain TEXT,
  industry TEXT,
  employee_count INTEGER,
  revenue_range TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  country TEXT,
  timezone TEXT,
  company_type TEXT NOT NULL DEFAULT 'prospect',
  relationship_types JSONB DEFAULT '[]'::jsonb,
  hub_instance_url TEXT,
  storefront_ids JSONB DEFAULT '[]'::jsonb,
  si_entity_id TEXT,
  source TEXT DEFAULT 'manual',
  billing_email TEXT,
  billing_address TEXT,
  health_score INTEGER DEFAULT 50,
  engagement_score DOUBLE PRECISION DEFAULT 0,
  close_id TEXT,
  close_url TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  import_batch_id TEXT
);

CREATE TABLE crm_contacts (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  company_id TEXT,
  email TEXT,
  first_name TEXT,
  last_name TEXT,
  full_name TEXT,
  title TEXT,
  role TEXT,
  department TEXT,
  phone TEXT,
  contact_type TEXT DEFAULT 'end_user',
  source TEXT DEFAULT 'manual',
  source_contact_id TEXT,
  source_artifact_id TEXT,
  investor_profile_id TEXT,
  pipeline_stage TEXT,
  funnel_stage TEXT,
  engagement_score DOUBLE PRECISION DEFAULT 0,
  last_engagement_at TIMESTAMPTZ,
  enrichment_status TEXT DEFAULT 'pending',
  enrichment_data JSONB DEFAULT '{}'::jsonb,
  linkedin_url TEXT,
  photo_url TEXT,
  close_lead_id TEXT,
  close_contact_id TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  import_batch_id TEXT
);

CREATE TABLE crm_activities (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  company_id TEXT,
  contact_id TEXT,
  activity_type TEXT NOT NULL,
  title TEXT,
  description TEXT,
  source_table TEXT,
  source_id TEXT,
  agent_id TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crm_relationships (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  from_company_id TEXT NOT NULL,
  to_company_id TEXT NOT NULL,
  relationship_type TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crm_signal_dismissals (
  id TEXT PRIMARY KEY,
  signal_key TEXT NOT NULL,
  user_email TEXT NOT NULL,
  action TEXT DEFAULT 'dismiss',
  snooze_until TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE status_checks (
  id TEXT PRIMARY KEY,
  service TEXT NOT NULL,
  endpoint TEXT,
  status TEXT DEFAULT 'up',
  response_ms INTEGER DEFAULT 0,
  status_code INTEGER,
  error_message TEXT,
  checked_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE status_incidents (
  id TEXT PRIMARY KEY,
  service TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  severity TEXT DEFAULT 'minor',
  status TEXT DEFAULT 'investigating',
  started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  resolved_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE import_batches (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  source TEXT NOT NULL,
  imported_by TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'processing',
  total_records INTEGER DEFAULT 0,
  valid_records INTEGER DEFAULT 0,
  imported_records INTEGER DEFAULT 0,
  merged_records INTEGER DEFAULT 0,
  dropped_records INTEGER DEFAULT 0,
  enriched_records INTEGER DEFAULT 0,
  error_details TEXT,
  summary TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMPTZ
);

CREATE TABLE import_links (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  token TEXT NOT NULL UNIQUE,
  created_by TEXT NOT NULL,
  label TEXT,
  scopes JSONB DEFAULT '["contacts"]'::jsonb,
  max_uses INTEGER DEFAULT 1,
  use_count INTEGER DEFAULT 0,
  expires_at TIMESTAMPTZ NOT NULL,
  used_at TIMESTAMPTZ,
  ip_address TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE competitor_domains (
  domain TEXT PRIMARY KEY,
  company_name TEXT,
  added_by TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE enrichment_log (
  id TEXT PRIMARY KEY,
  contact_id TEXT,
  company_id TEXT,
  source TEXT NOT NULL,
  request_type TEXT,
  response_status INTEGER,
  fields_filled TEXT,
  fields_skipped TEXT,
  cost_credits DOUBLE PRECISION DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_templates (
  id TEXT PRIMARY KEY,
  slug TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,
  category TEXT DEFAULT 'operations',
  skill_prompt TEXT NOT NULL,
  data_needs JSONB DEFAULT '[]'::jsonb,
  required_connectors JSONB DEFAULT '[]'::jsonb,
  tools JSONB DEFAULT '[]'::jsonb,
  sections JSONB DEFAULT '[]'::jsonb,
  domain_keywords JSONB DEFAULT '[]'::jsonb,
  model TEXT DEFAULT 'claude-sonnet-4-6',
  default_autonomy_level INTEGER DEFAULT 1,
  jockey_capable INTEGER DEFAULT 0,
  brain_context INTEGER DEFAULT 0,
  version INTEGER DEFAULT 1,
  changelog TEXT,
  created_by TEXT DEFAULT 'system',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_instances (
  id TEXT PRIMARY KEY,
  template_id TEXT NOT NULL,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  agent_config_id TEXT,
  prompt_overrides TEXT DEFAULT '',
  connected_data_sources JSONB DEFAULT '[]'::jsonb,
  custom_sections JSONB DEFAULT '[]'::jsonb,
  autonomy_level INTEGER DEFAULT 1,
  pinned_version INTEGER,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (template_id) REFERENCES agent_templates(id)
);

CREATE TABLE pricing_addons (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  price_cents INTEGER NOT NULL,
  billing_type TEXT NOT NULL DEFAULT 'recurring',
  billing_interval TEXT DEFAULT 'monthly',
  tier_requirement TEXT,
  stripe_price_id TEXT,
  category TEXT,
  active INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subscription_addons (
  id BIGSERIAL PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  addon_id TEXT NOT NULL REFERENCES pricing_addons(id),
  status TEXT NOT NULL DEFAULT 'active',
  quantity INTEGER NOT NULL DEFAULT 1,
  stripe_subscription_item_id TEXT,
  started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  cancelled_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(tenant_id, addon_id)
);

CREATE TABLE subscription_changes (
  id BIGSERIAL PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  change_type TEXT NOT NULL,
  old_plan TEXT,
  new_plan TEXT,
  addon_id TEXT,
  stripe_event_id TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE saas_replacement_map (
  id BIGSERIAL PRIMARY KEY,
  tool_name TEXT NOT NULL,
  tool_aliases JSONB,
  category TEXT NOT NULL,
  hub_agent_id TEXT,
  hub_agent_display TEXT,
  avg_monthly_cost_cents INTEGER,
  business_types JSONB,
  active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE onboarding_savings (
  id BIGSERIAL PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  tool_name TEXT NOT NULL,
  category TEXT NOT NULL,
  reported_cost_cents INTEGER NOT NULL DEFAULT 0,
  hub_replacement TEXT,
  source TEXT DEFAULT 'self_reported',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE deploy_verifications (
  id TEXT PRIMARY KEY,
  git_sha TEXT,
  session_id TEXT,
  triggered_by TEXT DEFAULT 'manual',
  total_checks INTEGER DEFAULT 0,
  passed INTEGER DEFAULT 0,
  failed INTEGER DEFAULT 0,
  overall TEXT DEFAULT 'unknown',
  results_json JSONB,
  created_at TIMESTAMPTZ,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE user_patterns (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  user_email TEXT NOT NULL,
  pattern_type TEXT NOT NULL,
  pattern TEXT NOT NULL,
  confidence DOUBLE PRECISION DEFAULT 1.0,
  source TEXT DEFAULT 'seeded',
  is_active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hub_relationships (
  id TEXT PRIMARY KEY,
  parent_tenant_id TEXT NOT NULL,
  child_tenant_id TEXT NOT NULL,
  relationship_type TEXT DEFAULT 'subsidiary',
  permissions_json JSONB DEFAULT '{}'::jsonb,
  status TEXT DEFAULT 'active',
  created_by TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(parent_tenant_id, child_tenant_id)
);

CREATE TABLE audit_findings (
  id TEXT PRIMARY KEY,
  category TEXT NOT NULL DEFAULT 'code',
  severity TEXT NOT NULL DEFAULT 'info',
  title TEXT NOT NULL,
  description TEXT,
  file_path TEXT,
  line_number INTEGER,
  status TEXT NOT NULL DEFAULT 'open',
  found_by TEXT DEFAULT 'hc_auditor',
  fixed_by TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  resolved_at TIMESTAMPTZ,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode'
);

CREATE TABLE audit_runs (
  id TEXT PRIMARY KEY,
  run_type TEXT NOT NULL DEFAULT 'full',
  findings_count INTEGER DEFAULT 0,
  critical_count INTEGER DEFAULT 0,
  warning_count INTEGER DEFAULT 0,
  info_count INTEGER DEFAULT 0,
  duration_ms INTEGER,
  triggered_by TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode'
);

CREATE TABLE build_items (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL DEFAULT 'bug',
  title TEXT NOT NULL,
  description TEXT,
  severity TEXT NOT NULL DEFAULT 'medium',
  status TEXT NOT NULL DEFAULT 'open',
  assigned_agent TEXT,
  session_id TEXT,
  created_by TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode',
  wave TEXT DEFAULT 'w1_now',
  item_type TEXT DEFAULT 'bug',
  project TEXT DEFAULT 'hub',
  screenshot_url TEXT,
  reporter_email TEXT,
  fix_notes TEXT,
  session_prompt TEXT,
  qa_result TEXT,
  page_url TEXT,
  priority INTEGER DEFAULT 3
);

CREATE TABLE build_tests (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  test_type TEXT NOT NULL DEFAULT 'manual',
  status TEXT NOT NULL DEFAULT 'pending',
  result_notes TEXT,
  linked_build_item_id TEXT,
  created_by TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode'
);

CREATE TABLE build_notes (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT,
  created_by TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  tenant_id TEXT NOT NULL DEFAULT 'sprint_mode'
);

CREATE TABLE deel_payments (
  id TEXT PRIMARY KEY,
  contractor_id TEXT,
  contract_id TEXT,
  amount DOUBLE PRECISION DEFAULT 0,
  currency TEXT DEFAULT 'USD',
  status TEXT DEFAULT 'pending',
  payment_type TEXT DEFAULT 'monthly',
  period_start TEXT,
  period_end TEXT,
  submitted_at TIMESTAMPTZ,
  approved_at TIMESTAMPTZ,
  approved_by TEXT,
  paid_at TIMESTAMPTZ,
  deel_payment_id TEXT,
  notes TEXT,
  tenant_id TEXT DEFAULT 'sprint_mode',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE storefront_agent_map (
  id TEXT PRIMARY KEY,
  storefront_id TEXT NOT NULL,
  agent_config_id TEXT NOT NULL,
  activation_rule TEXT DEFAULT 'auto',
  priority INTEGER DEFAULT 0,
  custom_prompt_override TEXT,
  custom_data_tables TEXT,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (storefront_id) REFERENCES storefront_brands(id),
  FOREIGN KEY (agent_config_id) REFERENCES agent_configs(id)
);

CREATE TABLE cadence_templates (
  id TEXT PRIMARY KEY,
  tenant_id TEXT DEFAULT 'sprint_mode',
  name TEXT NOT NULL,
  steps_json JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cadence_log (
  id TEXT PRIMARY KEY,
  sequence_id TEXT NOT NULL,
  step_number INTEGER NOT NULL,
  action TEXT NOT NULL,
  email_id TEXT,
  result TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE investor_engagement_log (
  id TEXT PRIMARY KEY,
  investor_id TEXT NOT NULL,
  viewer_email TEXT NOT NULL,
  page TEXT,
  event TEXT NOT NULL,
  notified_to TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fundraise_campaigns (
  id TEXT PRIMARY KEY,
  tenant_id TEXT DEFAULT 'sprint_mode',
  name TEXT NOT NULL,
  raise_id TEXT,
  icp_description TEXT,
  instrument TEXT,
  valuation_cap DOUBLE PRECISION,
  min_check DOUBLE PRECISION,
  cadence_template_id TEXT,
  status TEXT DEFAULT 'draft',
  stats_json JSONB DEFAULT '{}'::jsonb,
  playbook_json JSONB DEFAULT '[]'::jsonb,
  created_by TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fundraise_campaign_prospects (
  id TEXT PRIMARY KEY,
  campaign_id TEXT NOT NULL,
  investor_id TEXT NOT NULL,
  sequence_id TEXT,
  page_token TEXT,
  page_artifact_id TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prospect_decisions (
  id TEXT PRIMARY KEY,
  tenant_id TEXT DEFAULT 'sprint_mode',
  investor_id TEXT NOT NULL,
  campaign_id TEXT,
  decision TEXT NOT NULL CHECK(decision IN ('approve','reject','skip')),
  reason TEXT,
  decided_by TEXT NOT NULL,
  attributes_json JSONB,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE network_connections (
  id TEXT PRIMARY KEY,
  tenant_id TEXT DEFAULT 'sprint_mode',
  owner_email TEXT NOT NULL,
  owner_name TEXT,
  connection_name TEXT NOT NULL,
  connection_email TEXT,
  connection_linkedin TEXT,
  connection_company TEXT,
  connection_title TEXT,
  relationship TEXT,
  source TEXT,
  imported_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE event_triggers (
  id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  agent_id TEXT NOT NULL,
  filter_json JSONB,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE brief_cards (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  agent_id TEXT NOT NULL,
  title TEXT,
  body TEXT,
  zone TEXT,
  priority INTEGER DEFAULT 5,
  action_label TEXT,
  action_type TEXT,
  action_payload TEXT,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hub_registry (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  hostname TEXT NOT NULL,
  db_binding TEXT NOT NULL,
  db_id TEXT,
  owner_email TEXT,
  plan TEXT DEFAULT 'start',
  status TEXT DEFAULT 'active',
  tenant_id TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE webauthn_credentials (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  credential_id TEXT NOT NULL UNIQUE,
  public_key TEXT NOT NULL,
  sign_count INTEGER DEFAULT 0,
  transports TEXT,
  device_name TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT
);

CREATE TABLE user_identity_links (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  email_type TEXT DEFAULT 'work',
  is_primary INTEGER DEFAULT 0,
  verified INTEGER DEFAULT 1,
  linked_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  linked_by TEXT
);

CREATE TABLE saas_tools (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  monthly_cost DOUBLE PRECISION DEFAULT 0,
  hub_replacement TEXT,
  hub_replacement_status TEXT DEFAULT 'not_started',
  category TEXT,
  notes TEXT,
  tenant_id TEXT DEFAULT 'sprint_mode',
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
);

CREATE TABLE elle_journeys (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  agent_id TEXT NOT NULL,
  trigger_type TEXT NOT NULL,
  trigger_filter TEXT,
  steps_json JSONB NOT NULL,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE TABLE elle_runs (
  id TEXT PRIMARY KEY,
  journey_id TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'running',
  total_steps INTEGER DEFAULT 0,
  passed_steps INTEGER DEFAULT 0,
  failed_steps INTEGER DEFAULT 0,
  score DOUBLE PRECISION DEFAULT 0,
  results_json JSONB,
  error TEXT,
  duration_ms INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  FOREIGN KEY (journey_id) REFERENCES elle_journeys(id)
);

CREATE TABLE elle_assertions (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  step_index INTEGER NOT NULL,
  step_name TEXT,
  assertion_type TEXT NOT NULL,
  expected TEXT,
  actual TEXT,
  passed INTEGER DEFAULT 0,
  error TEXT,
  duration_ms INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (run_id) REFERENCES elle_runs(id)
);

CREATE TABLE elle_agent_scores (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  total_journeys INTEGER DEFAULT 0,
  passed_journeys INTEGER DEFAULT 0,
  failed_journeys INTEGER DEFAULT 0,
  consecutive_passes INTEGER DEFAULT 0,
  consecutive_fails INTEGER DEFAULT 0,
  correction_rate_50 DOUBLE PRECISION DEFAULT 0,
  correction_rate_200 DOUBLE PRECISION DEFAULT 0,
  correction_rate_1000 DOUBLE PRECISION DEFAULT 0,
  last_run_id TEXT,
  last_run_status TEXT,
  last_run_at TIMESTAMPTZ,
  recommended_level INTEGER DEFAULT 1,
  current_level INTEGER DEFAULT 1,
  security_violations INTEGER DEFAULT 0,
  last_demotion_at TIMESTAMPTZ,
  last_promotion_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode',
  UNIQUE(agent_id, tenant_id)
);

CREATE TABLE stream_entries (
  id TEXT PRIMARY KEY,
  hub_id TEXT NOT NULL DEFAULT 'sprint_mode',
  source_type TEXT NOT NULL,
  source_id TEXT,
  agent_id TEXT,
  user_email TEXT,
  event_type TEXT NOT NULL,
  summary TEXT,
  payload_json JSONB,
  visibility TEXT DEFAULT 'team',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  tenant_id TEXT DEFAULT 'sprint_mode'
);

CREATE INDEX idx_people_email ON people(email);

CREATE INDEX idx_clients_entity ON clients(entity_id);

CREATE INDEX idx_clients_status ON clients(status);

CREATE INDEX idx_clients_health ON clients(health);

CREATE INDEX idx_investors_pipeline ON investors(pipeline_type);

CREATE INDEX idx_investors_entity ON investors(entity_id);

CREATE INDEX idx_investors_stage ON investors(stage);

CREATE INDEX idx_investors_owner ON investors(owner);

CREATE INDEX idx_deals_entity ON deals(entity_id);

CREATE INDEX idx_deals_stage ON deals(stage);

CREATE INDEX idx_initiatives_entity ON initiatives(entity_id);

CREATE INDEX idx_initiatives_status ON initiatives(status);

CREATE INDEX idx_initiatives_owner ON initiatives(owner);

CREATE INDEX idx_milestones_initiative ON milestones(initiative_id);

CREATE INDEX idx_tasks_owner ON tasks(owner);

CREATE INDEX idx_tasks_entity ON tasks(entity_id);

CREATE INDEX idx_tasks_status ON tasks(status);

CREATE INDEX idx_decisions_entity ON decisions(entity_id);

CREATE INDEX idx_approvals_entity ON approvals(entity_id);

CREATE INDEX idx_approvals_status ON approvals(status);

CREATE INDEX idx_approvals_assigned ON approvals(assigned_to);

CREATE INDEX idx_documents_entity ON documents(entity_id);

CREATE INDEX idx_documents_category ON documents(category);

CREATE INDEX idx_governance_entity ON governance(entity_id);

CREATE INDEX idx_governance_status ON governance(status);

CREATE INDEX idx_finance_entity ON finance_snapshots(entity_id);

CREATE INDEX idx_finance_period ON finance_snapshots(period);

CREATE INDEX idx_events_actor ON events(actor);

CREATE INDEX idx_events_entity ON events(entity_id);

CREATE INDEX idx_events_created ON events(created_at);

CREATE INDEX idx_team_signals_email ON team_signals(person_email);

CREATE INDEX idx_notes_target ON notes(target_type, target_id);

CREATE UNIQUE INDEX idx_connector_configs_provider ON connector_configs(provider);

CREATE INDEX idx_sync_log_connector ON sync_log(connector_id);

CREATE INDEX idx_sync_log_started ON sync_log(started_at DESC);

CREATE UNIQUE INDEX idx_calendar_event_id ON calendar_events(event_id);

CREATE INDEX idx_calendar_connector ON calendar_events(connector_id);

CREATE INDEX idx_calendar_start ON calendar_events(start_time);

CREATE INDEX idx_calendar_entity ON calendar_events(entity_id);

CREATE UNIQUE INDEX idx_qb_txn_id ON qb_transactions(txn_id);

CREATE INDEX idx_qb_connector ON qb_transactions(connector_id);

CREATE INDEX idx_qb_date ON qb_transactions(date DESC);

CREATE INDEX idx_qb_entity ON qb_transactions(entity_id);

CREATE INDEX idx_qb_type ON qb_transactions(type);

CREATE INDEX idx_investor_users_email ON investor_users(email);

CREATE INDEX idx_investor_users_investor ON investor_users(investor_id);

CREATE INDEX idx_investor_updates_date ON investor_updates(date DESC);

CREATE INDEX idx_fund_metrics_period ON fund_metrics(period DESC);

CREATE INDEX idx_fund_documents_category ON fund_documents(category);

CREATE INDEX idx_investor_transactions_investor ON investor_transactions(investor_id);

CREATE INDEX idx_investor_transactions_date ON investor_transactions(date DESC);

CREATE INDEX idx_client_users_email ON client_users(email);

CREATE INDEX idx_client_users_client ON client_users(client_id);

CREATE INDEX idx_client_messages_client ON client_messages(client_id);

CREATE INDEX idx_client_messages_created ON client_messages(created_at);

CREATE INDEX idx_client_invoices_client ON client_invoices(client_id);

CREATE INDEX idx_client_invoices_status ON client_invoices(status);

CREATE INDEX idx_brief_deliveries_user
  ON brief_deliveries(user_email, delivered_at DESC);

CREATE INDEX idx_brief_deliveries_date
  ON brief_deliveries(delivered_at DESC);

CREATE INDEX idx_brief_prefs_tz
  ON brief_preferences(timezone);

CREATE INDEX idx_ask_conversations_user
  ON ask_conversations(user_email, updated_at DESC);

CREATE INDEX idx_ask_messages_conversation
  ON ask_messages(conversation_id, created_at ASC);

CREATE INDEX idx_signal_history_email_date
  ON team_signal_history (person_email, date DESC);

CREATE INDEX idx_signal_history_date
  ON team_signal_history (date DESC);

CREATE INDEX idx_email_templates_category ON email_templates(category);

CREATE INDEX idx_ask_actions_status ON ask_actions(status);

CREATE INDEX idx_ask_actions_conversation ON ask_actions(conversation_id);

CREATE INDEX idx_candidates_stage ON candidates(stage);

CREATE INDEX idx_candidates_entity ON candidates(entity_id);

CREATE INDEX idx_candidates_owner ON candidates(owner);

CREATE INDEX idx_workflow_runs_workflow ON workflow_runs(workflow_id);

CREATE INDEX idx_workflows_status ON workflows(status);

CREATE INDEX idx_cap_table_investor ON cap_table_entries(investor_profile_id);

CREATE INDEX idx_cap_table_type ON cap_table_entries(type);

CREATE INDEX idx_ir_calendar_status ON ir_calendar_items(status);

CREATE INDEX idx_ir_calendar_category ON ir_calendar_items(category);

CREATE INDEX idx_content_status ON content_items(status);

CREATE INDEX idx_comms_messages_thread ON comms_messages(thread_id);

CREATE INDEX idx_portal_activity_investor ON portal_activity_log(investor_profile_id);

CREATE INDEX idx_jockey_sessions_project ON jockey_sessions(project_id);

CREATE INDEX idx_jockey_sessions_status ON jockey_sessions(status);

CREATE INDEX idx_jockey_sessions_operator ON jockey_sessions(operator_id);

CREATE INDEX idx_jockey_sessions_created ON jockey_sessions(created_at);

CREATE INDEX idx_jockey_decisions_project ON jockey_decisions(project_id);

CREATE INDEX idx_jockey_decisions_status ON jockey_decisions(status);

CREATE INDEX idx_jockey_decisions_priority ON jockey_decisions(priority);

CREATE INDEX idx_jockey_skills_name ON jockey_skills(name);

CREATE INDEX idx_jockey_skills_project ON jockey_skills(project_id);

CREATE INDEX idx_jockey_evals_date ON jockey_evals(eval_date);

CREATE INDEX idx_jockey_evals_type ON jockey_evals(type);

CREATE INDEX idx_jockey_patterns_category ON jockey_patterns(category);

CREATE INDEX idx_notifications_user ON notifications(user_email);

CREATE INDEX idx_notifications_type ON notifications(type);

CREATE INDEX idx_notifications_read ON notifications(user_email, is_read);

CREATE INDEX idx_ask_conv_user ON ask_conversations(user_email, updated_at DESC);

CREATE INDEX idx_ask_msg_conv ON ask_messages(conversation_id, created_at ASC);

CREATE INDEX idx_emails_user ON emails(user_email);

CREATE INDEX idx_emails_received ON emails(received_at DESC);

CREATE INDEX idx_slack_sent ON slack_messages(sent_at DESC);

CREATE INDEX idx_connectors_user ON connectors(user_email);

CREATE INDEX idx_agent_runs_agent ON agent_runs(agent_id);

CREATE INDEX idx_agent_runs_user ON agent_runs(user_email);

CREATE INDEX idx_agent_runs_created ON agent_runs(created_at);

CREATE INDEX idx_agent_memory_agent ON agent_memory(agent_id);

CREATE INDEX idx_agent_memory_entity ON agent_memory(entity_type, entity_id);

CREATE INDEX idx_autonomy_agent ON autonomy_scores(agent_id, action_type);

CREATE INDEX idx_filings_due ON filing_deadlines(due_date);

CREATE INDEX idx_filings_status ON filing_deadlines(status);

CREATE INDEX idx_financial_scenarios_created ON financial_scenarios(created_at);

CREATE INDEX idx_transactions_date ON transactions(date);

CREATE INDEX idx_transactions_category ON transactions(category);

CREATE INDEX idx_transactions_vendor ON transactions(vendor);

CREATE INDEX idx_reconciliation_period ON reconciliation_log(period);

CREATE INDEX idx_deals_pipeline ON pipeline_deals(pipeline);

CREATE INDEX idx_deals_owner ON pipeline_deals(owner);

CREATE INDEX idx_outbound_status ON outbound_sequences(status);

CREATE INDEX idx_outbound_qualified ON outbound_sequences(qualified);

CREATE INDEX idx_outbound_messages_seq ON outbound_messages(sequence_id);

CREATE INDEX idx_comms_source ON communication_queue(source);

CREATE INDEX idx_comms_processed ON communication_queue(processed);

CREATE INDEX idx_comms_urgency ON communication_queue(urgency);

CREATE INDEX idx_client_health ON client_health_scores(health_score);

CREATE INDEX idx_client_churn ON client_health_scores(churn_risk);

CREATE INDEX idx_client_jockey ON client_jockey_configs(client_id);

CREATE INDEX idx_content_type ON content_library(content_type);

CREATE INDEX idx_patterns_type ON agent_patterns(pattern_type);

CREATE INDEX idx_patterns_agent ON agent_patterns(source_agent);

CREATE INDEX idx_calls_type ON call_transcripts(call_type);

CREATE INDEX idx_calls_processed ON call_transcripts(processed);

CREATE INDEX idx_calls_recorded ON call_transcripts(recorded_at);

CREATE INDEX idx_workflow_runs_status ON workflow_runs(status);

CREATE INDEX idx_workflow_runs_type ON workflow_runs(workflow_type);

CREATE INDEX idx_workflow_runs_triggered_by ON workflow_runs(triggered_by);

CREATE INDEX idx_hub_events_type ON hub_events(event_type);

CREATE INDEX idx_hub_events_actor ON hub_events(actor_id);

CREATE INDEX idx_hub_events_entity ON hub_events(entity_type, entity_id);

CREATE INDEX idx_hub_events_created ON hub_events(created_at);

CREATE INDEX idx_agent_runs_action ON agent_runs(action_taken, awaiting_approval, created_at);

CREATE INDEX idx_agent_runs_autonomy ON agent_runs(autonomy_level, action_taken, created_at);

CREATE UNIQUE INDEX idx_coa_account_number ON chart_of_accounts(account_number);

CREATE INDEX idx_bank_txn_date ON bank_transactions(date);

CREATE INDEX idx_bank_txn_matched ON bank_transactions(matched_qb_txn_id);

CREATE INDEX idx_bank_txn_plaid ON bank_transactions(plaid_transaction_id);

CREATE INDEX idx_recon_task_period ON reconciliation_tasks(period);

CREATE INDEX idx_recon_task_status ON reconciliation_tasks(status);

CREATE INDEX idx_monthly_close_period ON monthly_close(period);

CREATE INDEX idx_agent_kpis_agent ON agent_kpis(agent_id);

CREATE INDEX idx_agent_kpis_period ON agent_kpis(period);

CREATE INDEX idx_stripe_date ON stripe_transactions(date);

CREATE INDEX idx_ramp_date ON ramp_transactions(date);

CREATE UNIQUE INDEX idx_vendor_pattern ON vendor_rules(vendor_pattern);

CREATE INDEX idx_vault_items_tenant ON vault_items(tenant_id);

CREATE INDEX idx_vault_items_owner ON vault_items(owner);

CREATE INDEX idx_vault_items_category ON vault_items(category);

CREATE INDEX idx_vault_items_expires ON vault_items(expires_at);

CREATE INDEX idx_val_item ON vault_access_log(vault_item_id);

CREATE INDEX idx_val_time ON vault_access_log(created_at);

CREATE INDEX idx_vat_token ON vault_auth_tokens(token);

CREATE INDEX idx_vat_email ON vault_auth_tokens(user_email);

CREATE INDEX idx_aconv_lookup ON agent_conversations(tenant_id, agent_id, user_email, last_message_at);

CREATE INDEX idx_aruns_conv ON agent_runs(conversation_id);

CREATE INDEX idx_amem_user ON agent_memory(agent_id, user_email, is_active);

CREATE INDEX idx_hub_external_source ON hub_external_data (source_hub_url);

CREATE INDEX idx_hub_external_updated ON hub_external_data (updated_at);

CREATE INDEX idx_tool_audit_agent ON agent_tool_audit(agent_id, created_at);

CREATE INDEX idx_tool_audit_type ON agent_tool_audit(tool_type, created_at);

CREATE INDEX idx_sf_scopes_agent ON storefront_scopes(agent_id, created_at);

CREATE INDEX idx_sf_projects_scope ON storefront_projects(scope_id);

CREATE INDEX idx_sf_deliverables_project ON storefront_deliverables(project_id);

CREATE INDEX idx_priv_subs_email ON privacy_subscribers(email);

CREATE INDEX idx_priv_scans_sub ON privacy_scans(subscriber_id, created_at);

CREATE INDEX idx_priv_removals_sub ON privacy_removals(subscriber_id, status);

CREATE INDEX idx_sf_brands_slug ON storefront_brands(slug);

CREATE INDEX idx_sf_brands_agent ON storefront_brands(agent_id);

CREATE INDEX idx_gtm_brand ON storefront_gtm_configs(brand_slug);

CREATE INDEX idx_outbound_brand ON storefront_outbound_sequences(brand_slug);

CREATE INDEX idx_sf_eval_agent ON storefront_evaluations(agent_id);

CREATE INDEX idx_sf_eval_score ON storefront_evaluations(viability_score DESC);

CREATE INDEX idx_sfm_daily ON storefront_metrics_daily(brand_slug, date);

CREATE INDEX idx_sfx_brand ON storefront_experiments(brand_slug, status);

CREATE INDEX idx_saas_active ON saas_subscriptions(active, replacement_status);

CREATE INDEX idx_sf_prd_agent ON storefront_prds(agent_id);

CREATE INDEX idx_sf_prd_status ON storefront_prds(status);

CREATE INDEX idx_at_storefront ON agent_transactions(target_storefront, created_at);

CREATE INDEX idx_at_status ON agent_transactions(status);

CREATE INDEX idx_at_hub ON agent_transactions(source_hub_id, created_at);

CREATE INDEX idx_at_created ON agent_transactions(created_at);

CREATE INDEX idx_ns_processed ON narrative_signals(processed, created_at);

CREATE INDEX idx_nt_user ON narrative_threads(user_email, updated_at);

CREATE INDEX idx_nf_entity ON narrative_faqs(entity, audience);

CREATE INDEX idx_agent_actions_status ON agent_actions(status);

CREATE INDEX idx_agent_actions_agent ON agent_actions(agent_id);

CREATE INDEX idx_work_queue_status ON agent_work_queue(status, priority);

CREATE INDEX idx_work_queue_agent ON agent_work_queue(agent_id);

CREATE INDEX idx_uap_user ON user_agent_permissions(user_email);

CREATE INDEX idx_uap_agent ON user_agent_permissions(agent_id);

CREATE INDEX idx_brief_cache_user ON brief_cache(user_email);

CREATE INDEX idx_sc_brand ON storefront_customers(brand_slug);

CREATE INDEX idx_sc_status ON storefront_customers(status);

CREATE INDEX idx_cm_status ON client_migrations(status);

CREATE INDEX idx_vendor_rules_tenant ON vendor_rules(tenant_id);

CREATE INDEX idx_bank_txns_date_cat ON bank_transactions(date, hub_category);

CREATE INDEX idx_bank_txns_period_conf ON bank_transactions(date, hub_category_confidence);

CREATE INDEX idx_amu_agent ON agent_model_usage(agent_id);

CREATE INDEX idx_amu_model ON agent_model_usage(model);

CREATE INDEX idx_amu_created ON agent_model_usage(created_at);

CREATE INDEX idx_amu_tenant ON agent_model_usage(tenant_id);

CREATE INDEX idx_legal_matters_type ON legal_matters(matter_type);

CREATE INDEX idx_legal_matters_status ON legal_matters(status);

CREATE INDEX idx_legal_matters_owner ON legal_matters(owner);

CREATE INDEX idx_legal_matters_tenant ON legal_matters(tenant_id);

CREATE INDEX idx_slack_triage ON slack_messages(triage_status);

CREATE INDEX idx_comms_source_processed ON communication_queue(source, processed);

CREATE UNIQUE INDEX idx_sender_rep_lookup ON sender_reputation(sender, tenant_id);

CREATE INDEX idx_sender_rep_class ON sender_reputation(classification);

CREATE INDEX idx_eclass_from ON email_classifications(from_addr);

CREATE INDEX idx_eclass_class ON email_classifications(classification);

CREATE INDEX idx_outbound_slack_status ON outbound_slack_messages(status);

CREATE INDEX idx_outbound_slack_tenant ON outbound_slack_messages(tenant_id);

CREATE INDEX idx_shared_with ON shared_threads(shared_with, status);

CREATE INDEX idx_shared_conv ON shared_threads(conversation_id);

CREATE INDEX idx_shared_by ON shared_threads(shared_by);

CREATE UNIQUE INDEX idx_tgp_user_step ON tour_guide_progress(user_email, step_id);

CREATE INDEX idx_tgp_user ON tour_guide_progress(user_email, status);

CREATE UNIQUE INDEX idx_pagetip_user_page ON page_tips(user_email, page_id);

CREATE UNIQUE INDEX idx_fav_user ON feature_announcement_views(announcement_id, user_email);

CREATE UNIQUE INDEX idx_ufu_user_feature ON user_feature_usage(user_email, feature_key);

CREATE INDEX idx_ic_votes_deal ON ic_votes(deal_id);

CREATE INDEX idx_artifacts_agent ON agent_artifacts(agent_id);

CREATE INDEX idx_artifacts_user ON agent_artifacts(user_email);

CREATE INDEX idx_relay_to ON hub_relays(to_email, status);

CREATE INDEX idx_relay_from ON hub_relays(from_email, status);

CREATE INDEX idx_relay_status ON hub_relays(status);

CREATE INDEX idx_emails_thread ON emails(gmail_thread_id);

CREATE INDEX idx_emails_reply ON emails(reply_status);

CREATE UNIQUE INDEX idx_ethreads_gmail ON email_threads(gmail_thread_id, tenant_id);

CREATE INDEX idx_ethreads_assigned ON email_threads(assigned_user);

CREATE INDEX idx_deel_contractors_status ON deel_contractors(status);

CREATE INDEX idx_deel_invoices_contractor ON deel_invoices(contractor_id);

CREATE INDEX idx_voice_user ON voice_intakes(user_email, created_at);

CREATE INDEX idx_voice_intent ON voice_intakes(intent);

CREATE INDEX idx_agent_proposals_status ON agent_proposals(status);

CREATE INDEX idx_agent_proposals_proposed_by ON agent_proposals(proposed_by);

CREATE INDEX idx_agent_proposals_created ON agent_proposals(created_at);

CREATE INDEX idx_proposals_status ON agent_proposals(status);

CREATE INDEX idx_proposals_type ON agent_proposals(type);

CREATE INDEX idx_proposals_tenant ON agent_proposals(tenant_id);

CREATE INDEX idx_proposals_proposed_by ON agent_proposals(proposed_by);

CREATE INDEX idx_policies_type ON platform_policies(policy_type, status);

CREATE INDEX idx_violations_entity ON platform_violations(entity_type, entity_id);

CREATE INDEX idx_violations_status ON platform_violations(status);

CREATE INDEX idx_violations_severity ON platform_violations(severity);

CREATE INDEX idx_suspensions_agent ON agent_suspensions(agent_id, status);

CREATE INDEX idx_custom_sections_agent ON custom_sidebar_sections(agent_id, tenant_id);

CREATE INDEX idx_custom_sections_creator ON custom_sidebar_sections(created_by);

CREATE INDEX idx_section_shares_recipient ON sidebar_section_shares(shared_with, status);

CREATE INDEX idx_section_shares_section ON sidebar_section_shares(section_id);

CREATE UNIQUE INDEX idx_agent_actions_dedup
ON agent_actions(agent_id, target_table, target_id, operation)
WHERE status = 'pending';

CREATE INDEX idx_hk_entry_type ON hub_knowledge(entry_type);

CREATE INDEX idx_hk_section_slug ON hub_knowledge(section_slug);

CREATE INDEX idx_hk_assigned_to ON hub_knowledge(assigned_to);

CREATE INDEX idx_dg_file_path ON deployment_guards(file_path);

CREATE INDEX idx_dg_session_id ON deployment_guards(session_id);

CREATE INDEX idx_threads_lookup ON threads(tenant_id, agent_id, user_email, last_message_at);

CREATE INDEX idx_threads_participants ON threads(participants);

CREATE INDEX idx_threads_type ON threads(thread_type);

CREATE INDEX idx_threads_user ON threads(user_email, updated_at DESC);

CREATE INDEX idx_artifacts_brief_type ON agent_artifacts(brief_type);

CREATE INDEX idx_artifacts_assigned_to ON agent_artifacts(assigned_to);

CREATE INDEX idx_notif_user ON hub_notifications(user_email, read_at);

CREATE INDEX idx_relay_type ON hub_relays(relay_type, status);

CREATE INDEX idx_presence_status ON user_presence(tenant_id, status);

CREATE INDEX idx_retry_status ON retry_queue(status, created_at);

CREATE INDEX idx_page_analytics_email ON page_analytics(viewer_email);

CREATE INDEX idx_page_analytics_page ON page_analytics(page);

CREATE INDEX idx_page_analytics_event ON page_analytics(event);

CREATE INDEX idx_artifacts_published ON agent_artifacts(publish_status);

CREATE INDEX idx_rn_date ON release_notes(commit_date DESC);

CREATE INDEX idx_rn_session ON release_notes(session_id);

CREATE INDEX idx_rn_category ON release_notes(category);

CREATE INDEX idx_acc_chain ON agent_accountability_chain(chain_id, sequence_number);

CREATE INDEX idx_acc_agent ON agent_accountability_chain(agent_id);

CREATE INDEX idx_acc_tenant ON agent_accountability_chain(tenant_id);

CREATE INDEX idx_outbound_page_slug ON outbound_sequences(page_slug);

CREATE INDEX idx_outbound_content_type ON outbound_sequences(content_type);

CREATE INDEX idx_outbound_artifact ON outbound_sequences(artifact_id);

CREATE INDEX idx_outbound_tracked_url ON outbound_sequences(tracked_url);

CREATE INDEX idx_artifacts_brief ON agent_artifacts(brief_type, assigned_to);

CREATE INDEX idx_artifacts_assigned ON agent_artifacts(assigned_to);

CREATE INDEX idx_brief_actions_source ON brief_actions(source_id);

CREATE INDEX idx_brief_actions_assigned ON brief_actions(assigned_to, status);

CREATE INDEX idx_crm_companies_type ON crm_companies(company_type);

CREATE INDEX idx_crm_companies_domain ON crm_companies(domain);

CREATE INDEX idx_crm_companies_tenant ON crm_companies(tenant_id);

CREATE INDEX idx_crm_companies_source ON crm_companies(source);

CREATE INDEX idx_crm_companies_health ON crm_companies(health_score);

CREATE INDEX idx_crm_contacts_email ON crm_contacts(email);

CREATE INDEX idx_crm_contacts_company ON crm_contacts(company_id);

CREATE INDEX idx_crm_contacts_tenant ON crm_contacts(tenant_id);

CREATE INDEX idx_crm_contacts_type ON crm_contacts(contact_type);

CREATE INDEX idx_crm_contacts_source ON crm_contacts(source);

CREATE INDEX idx_crm_contacts_investor ON crm_contacts(investor_profile_id);

CREATE INDEX idx_crm_contacts_engagement ON crm_contacts(engagement_score);

CREATE INDEX idx_crm_activities_company ON crm_activities(company_id);

CREATE INDEX idx_crm_activities_contact ON crm_activities(contact_id);

CREATE INDEX idx_crm_activities_type ON crm_activities(activity_type);

CREATE INDEX idx_crm_activities_tenant ON crm_activities(tenant_id);

CREATE INDEX idx_crm_activities_created ON crm_activities(created_at);

CREATE INDEX idx_crm_rel_from ON crm_relationships(from_company_id);

CREATE INDEX idx_crm_rel_to ON crm_relationships(to_company_id);

CREATE INDEX idx_crm_rel_type ON crm_relationships(relationship_type);

CREATE INDEX idx_crm_sig_dismiss_key ON crm_signal_dismissals(signal_key);

CREATE INDEX idx_status_checks_service ON status_checks(service, checked_at);

CREATE INDEX idx_status_incidents_status ON status_incidents(status);

CREATE INDEX idx_import_batches_tenant ON import_batches(tenant_id);

CREATE INDEX idx_import_batches_status ON import_batches(status);

CREATE INDEX idx_import_links_token ON import_links(token);

CREATE INDEX idx_enrichment_log_contact ON enrichment_log(contact_id);

CREATE INDEX idx_enrichment_log_source ON enrichment_log(source);

CREATE INDEX idx_agent_instances_tenant ON agent_instances(tenant_id);

CREATE INDEX idx_agent_instances_template ON agent_instances(template_id);

CREATE UNIQUE INDEX idx_agent_instances_tenant_template ON agent_instances(tenant_id, template_id);

CREATE INDEX idx_sub_addons_tenant ON subscription_addons(tenant_id);

CREATE INDEX idx_sub_changes_tenant ON subscription_changes(tenant_id);

CREATE INDEX idx_sub_changes_type ON subscription_changes(change_type);

CREATE INDEX idx_onboard_savings_tenant ON onboarding_savings(tenant_id);

CREATE INDEX idx_saas_map_category ON saas_replacement_map(category);

CREATE INDEX idx_deploy_verifications_created ON deploy_verifications(created_at);

CREATE INDEX idx_user_patterns_email ON user_patterns(user_email, is_active);

CREATE INDEX idx_hub_rel_parent ON hub_relationships(parent_tenant_id);

CREATE INDEX idx_hub_rel_child ON hub_relationships(child_tenant_id);

CREATE INDEX idx_audit_findings_status ON audit_findings(status);

CREATE INDEX idx_audit_findings_severity ON audit_findings(severity);

CREATE INDEX idx_build_items_status ON build_items(status);

CREATE INDEX idx_build_items_type ON build_items(type);

CREATE INDEX idx_build_tests_status ON build_tests(status);

CREATE INDEX idx_ci_stripe ON client_invoices(stripe_invoice_id);

CREATE INDEX idx_clients_stripe ON clients(stripe_customer_id);

CREATE INDEX idx_deel_payments_status ON deel_payments(status);

CREATE INDEX idx_deel_payments_contractor ON deel_payments(contractor_id);

CREATE INDEX idx_deel_payments_tenant ON deel_payments(tenant_id);

CREATE INDEX idx_sf_agent_map_storefront ON storefront_agent_map(storefront_id);

CREATE INDEX idx_sf_agent_map_agent ON storefront_agent_map(agent_config_id);

CREATE UNIQUE INDEX idx_sf_agent_map_unique ON storefront_agent_map(storefront_id, agent_config_id);

CREATE INDEX idx_cadlog_seq ON cadence_log(sequence_id);

CREATE INDEX idx_iel_investor ON investor_engagement_log(investor_id);

CREATE INDEX idx_iel_email ON investor_engagement_log(viewer_email);

CREATE INDEX idx_fc_tenant ON fundraise_campaigns(tenant_id);

CREATE INDEX idx_fc_status ON fundraise_campaigns(status);

CREATE INDEX idx_fcp_campaign ON fundraise_campaign_prospects(campaign_id);

CREATE INDEX idx_fcp_investor ON fundraise_campaign_prospects(investor_id);

CREATE INDEX idx_pd_campaign ON prospect_decisions(campaign_id);

CREATE INDEX idx_pd_decision ON prospect_decisions(decision);

CREATE INDEX idx_pd_investor ON prospect_decisions(investor_id);

CREATE INDEX idx_nc_owner ON network_connections(owner_email);

CREATE INDEX idx_nc_connection ON network_connections(connection_email);

CREATE INDEX idx_nc_linkedin ON network_connections(connection_linkedin);

CREATE INDEX idx_brief_cards_user_status ON brief_cards(user_email, status, created_at);

CREATE INDEX idx_webauthn_user ON webauthn_credentials(user_email);

CREATE INDEX idx_uil_user ON user_identity_links(user_id);

CREATE INDEX idx_uil_email ON user_identity_links(email);

CREATE INDEX idx_elle_runs_journey ON elle_runs(journey_id, created_at);

CREATE INDEX idx_elle_runs_status ON elle_runs(status);

CREATE INDEX idx_elle_assertions_run ON elle_assertions(run_id, step_index);

CREATE INDEX idx_elle_agent_scores_agent ON elle_agent_scores(agent_id);

CREATE INDEX idx_elle_agent_scores_level ON elle_agent_scores(recommended_level);

CREATE INDEX idx_stream_entries_source ON stream_entries(source_type, created_at);

CREATE INDEX idx_stream_entries_agent ON stream_entries(agent_id, created_at);

CREATE INDEX idx_stream_entries_event ON stream_entries(event_type, created_at);

CREATE INDEX idx_emails_listener ON emails(listener_processed, created_at);

CREATE INDEX idx_calendar_listener ON calendar_events(listener_processed, created_at);
