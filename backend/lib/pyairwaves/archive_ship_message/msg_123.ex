defmodule Pyairwaves.ArchiveShipMessage.Msg123 do
  use Ecto.Schema

  # Class A AIS Position Report
  embedded_schema do
    # AIS
    field :cog, :float
    field :communication_state, :integer
    field :latitude, :float
    field :longitude, :float
    field :navigational_status, :integer
    field :position_accuracy, :integer
    field :raim_flag, :integer
    field :rate_of_turn, :integer
    field :repeat_indicator, :integer
    field :sog, :float
    field :spare, :integer
    field :special_maneuvre_indicator, :integer
    field :time_stamp, :integer
    field :true_heading, :integer
    field :user_id, :integer
    # Specific NMEA
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
