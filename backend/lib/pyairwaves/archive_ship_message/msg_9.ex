defmodule Pyairwaves.ArchiveShipMessage.Msg9 do
  use Ecto.Schema

  # AIS Standard Search And Rescue Aircraft Position Report
  embedded_schema do
    field :altitude, :integer
    field :altitude_sensor, :integer
    field :assigned_mode_flag, :integer
    field :channel, :string
    field :checksum, :string
    field :cog, :float
    field :communication_state, :integer
    field :communication_state_selector_flag, :integer
    field :current, :string
    field :formatter, :string
    field :latitude, :float
    field :longitude, :float
    field :message_id, :integer
    field :padding, :string
    field :payload, :string
    field :position_accuracy, :integer
    field :raim_flag, :integer
    field :repeat_indicator, :integer
    field :sequential, :string
    field :sog, :integer
    field :spare1, :integer
    field :spare2, :integer
    field :talker, :string
    field :time_stamp, :integer
    field :total, :string
    field :user_id, :integer
  end
end
