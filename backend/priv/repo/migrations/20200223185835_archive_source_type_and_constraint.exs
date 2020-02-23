defmodule Pyairwaves.Repo.Migrations.ArchiveSourceTypeAndConstraint do
  use Ecto.Migration

  def change do
    drop unique_index(:archive_source, [:name])
    alter table("archive_source") do
      add :type, :string
    end
    create unique_index(:archive_source, [:name, :type])
  end
end
