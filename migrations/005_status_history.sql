
create table if not exists order_status_history (
  id bigserial primary key,
  order_id bigint not null references orders(id) on delete cascade,
  status text not null,
  changed_at timestamptz default now()
);
create index if not exists order_status_history_order_idx on order_status_history(order_id);
