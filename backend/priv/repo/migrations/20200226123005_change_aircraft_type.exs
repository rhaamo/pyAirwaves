defmodule Pyairwaves.Repo.Migrations.ChangeAircraftType do
  use Ecto.Migration

  def up do
    alter table("aircraft") do
      modify :type, :text
    end
  end

  def down do
    alter table("aircraft") do
      modify :type, :string, size: 255
    end
  end
end
