defmodule PyairwavesWeb.Router do
  use PyairwavesWeb, :router
  use Plug.ErrorHandler
  use Sentry.PlugCapture

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", PyairwavesWeb do
    pipe_through :browser

    get "/", MapController, :map
    get "/about", AppController, :about

    get "/archives/sources/coverage", ArchiveController, :sources_coverage

    # temp
    get "/archives/ais/quick", ArchiveController, :ais_quick
    get "/archives/adsb/quick", ArchiveController, :adsb_quick
  end

  # Other scopes may use custom stacks.
  # scope "/api", PyairwavesWeb do
  #   pipe_through :api
  # end
end
