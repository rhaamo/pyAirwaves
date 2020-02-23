defmodule Pyairwaves.Repo.Migrations.AddUuidExtension do
  use Ecto.Migration
  require Logger

  def up do
    Logger.warn("ATTENTION ATTENTION ATTENTION\n")

    Logger.warn(
      "This will try to create the uuid-ossp extension on your database. If your database user does NOT have the necessary rights, you will have to do it manually and re-run the migrations.\nYou can probably do this by running the following:\n"
    )

    Logger.warn(
      "sudo -u postgres psql pyairwaves -c \"create extension if not exists uuid-ossp\"\n"
    )

    execute("create extension if not exists \"uuid-ossp\"")
  end

  def down do
    execute("drop extension if exists \"uuid-ossp\"")
  end
end
