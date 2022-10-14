CREATE TABLE IF NOT EXISTS "backtest_metrics" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "return" float,
  "no_of_trades" int,
  "winning_trades" float,
  "losing_trades" float,
  "max_drawndown" float,
  "shape_ration" float,
  "scene_id" int
);

CREATE TABLE IF NOT EXISTS "scene" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "from_date" datetime,
  "to_date" datetime,
  "indicator_id" int
);

CREATE TABLE IF NOT EXISTS "indicator" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "indicator name" varchar NOT NULL,
  "param_from" float,
  "param_to" float
);

-- CREATE TABLE IF NOT EXISTS "indicator_param" (
--   "id" SERIAL PRIMARY KEY NOT NULL,
--   "param_name" varchar NOT NULL
-- );

CREATE TABLE  IF NOT EXISTS "users" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "full_name" varchar NOT NULL,
  "email" varchar NOT NULL,
  "password" varchar NOT NULL,
  "created_at" timestamp NOT NULL
);

ALTER TABLE "backtest_metrics" ADD FOREIGN KEY ("scene_id") REFERENCES "scene" ("id");

ALTER TABLE "indicator" ADD FOREIGN KEY ("id") REFERENCES "scene" ("id");

ALTER TABLE "indicator_param" ADD FOREIGN KEY ("id") REFERENCES "indicator" ("id");