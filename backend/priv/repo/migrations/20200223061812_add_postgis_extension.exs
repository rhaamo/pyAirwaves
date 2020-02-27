defmodule Pyairwaves.Repo.Migrations.AddPostgisExtension do
  use Ecto.Migration
  require Logger

  def up do
    Logger.warn("ATTENTION ATTENTION ATTENTION\n")

    Logger.warn(
      "This will try to create the postgis extension on your database. If your database user does NOT have the necessary rights, you will have to do it manually and re-run the migrations.\nYou can probably do this by running the following:\n"
    )

    Logger.warn(
      "sudo -u postgres psql pyairwaves -c \"create extension if not exists postgis\"\n"
    )

    execute("create extension if not exists postgis")
  end

  def down do
    execute("drop extension if exists postgis")
  end
end
