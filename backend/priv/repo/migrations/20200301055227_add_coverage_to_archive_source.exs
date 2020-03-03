defmodule Pyairwaves.Repo.Migrations.AddCoverageToArchiveSource do
  use Ecto.Migration

  def up do
    alter table(:archive_source) do
      add :coverage, {:array, :map}, default: []
    end
  end

  def down do
    alter table(:archive_source) do
      remove :coverage
    end
  end
end
