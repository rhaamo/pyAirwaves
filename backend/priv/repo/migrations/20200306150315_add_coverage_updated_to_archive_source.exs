defmodule Pyairwaves.Repo.Migrations.AddCoverageUpdatedToArchiveSource do
  use Ecto.Migration

  def up do
    alter table(:archive_source) do
      add :coverage_updated_at, :naive_datetime
    end
  end

  def down do
    alter table(:archive_source) do
      remove :coverage_updated_at
    end
  end
end
