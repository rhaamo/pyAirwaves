defmodule Pyairwaves.ArchiveShipMessage.Msg9 do
  use Ecto.Schema

  # AIS Standard Search And Rescue Aircraft Position Report
  embedded_schema do
    # AIS
    field :altitude, :integer
    field :altitude_sensor, :integer
    field :assigned_mode_flag, :integer
    field :cog, :float
    field :communication_state, :integer
    field :communication_state_selector_flag, :integer
    field :latitude, :float
    field :longitude, :float
    field :position_accuracy, :integer
    field :raim_flag, :integer
    field :repeat_indicator, :integer
    field :sog, :integer
    field :spare1, :integer
    field :spare2, :integer
    field :time_stamp, :integer
    field :user_id, :integer
    field :dte, :integer

    # NMEA
    field :channel, :string
    field :checksum, :string
    field :current, :string
    field :formatter, :string
    field :message_id, :integer
    field :padding, :string
    field :payload, :string
    field :talker, :string
    field :total, :string
    field :sequential, :string

  end
end
