defmodule Pyairwaves.Repo.Migrations.RenameConstraint do
  use Ecto.Migration

  def change do
    drop unique_index(:archive_source, [:name, :type])
    create unique_index(:archive_source, [:name, :type], name: :unique_name_type)
  end
end
