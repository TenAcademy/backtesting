CREATE TABLE "backtest_metrics" (
  "id" SERIAL PRIMARY KEY,
  "return" float,
  "no_of_trades" int,
  "winning_trades" float,
  "losing_trades" float,
  "max_drawndown" float,
  "shape_ration" float,
  "scene_id" int
);

CREATE TABLE "scene" (
  "id" SERIAL PRIMARY KEY,
  "from_date" datetime,
  "to_date" datetime,
  "indicator_id" int
);

CREATE TABLE "indicator" (
  "id" SERIAL PRIMARY KEY,
  "param_from" float,
  "param_to" float
);

CREATE TABLE "indicator_param" (
  "id" SERIAL PRIMARY KEY,
  "param_name" varchar
);

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "full_name" varchar,
  "email" varchar,
  "password" varchar,
  "created_at" timestamp
);

ALTER TABLE "backtest_metrics" ADD FOREIGN KEY ("scene_id") REFERENCES "scene" ("id");

ALTER TABLE "indicator" ADD FOREIGN KEY ("id") REFERENCES "scene" ("id");

ALTER TABLE "indicator_param" ADD FOREIGN KEY ("id") REFERENCES "indicator" ("id");