defmodule Pyairwaves.Translation do
  use Ecto.Schema

  @primary_key {:id, :id, autogenerate: true}

  schema "translation" do
    field :reg, :string, size: 20
    field :reg_correct, :string, size: 20
    field :operator, :string, size: 20
    field :operator_correct, :string, size: 20
    field :source, :string, size: 255
    timestamps()
  end
end
