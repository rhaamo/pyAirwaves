defmodule Pyairwaves.Repo.Migrations.CreateArchiveSource do
  use Ecto.Migration

  def change do
    create_if_not_exists table("archive_source") do
      add :name, :string
      add :geom, :geometry
      add :position_mode, :integer, default: 0

      # has_many :archive_ship_messages

      timestamps()
    end
  end
end
