defmodule Pyairwaves.ArchiveShipMessage.Msg123 do
  use Ecto.Schema

  # Class A AIS Position Report
  embedded_schema do
    field :channel, :string
    field :checksum, :string
    field :cog, :float
    field :communication_state, :integer
    field :current, :string
    field :formatter, :string
    field :latitude, :float
    field :longitude, :float
    field :message_id, :integer
    field :navigational_status, :integer
    field :padding, :string
    field :payload, :string
    field :position_accuracy, :integer
    field :raim_flag, :integer
    field :rate_of_turn, :integer
    field :repeat_indicator, :integer
    field :sequential, :string
    field :sog, :float
    field :spare, :integer
    field :special_maneuvre_indicator, :integer
    field :talker, :string
    field :time_stamp, :integer
    field :total, :string
    field :true_heading, :integer
    field :user_id, :integer
  end
end
