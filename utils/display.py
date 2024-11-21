import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import utils.convert as convert
import Dynamics.dynamics as dyn

def state_vec(name, state, sigfigs=6):
    print(f"{name} State Vector:")
    print(f"R: [{state[0]:.{sigfigs}}, {state[1]:.{sigfigs}}, {state[2]:.{sigfigs}}] m")
    print(f"V: [{state[3]:.{sigfigs}}, {state[4]:.{sigfigs}}, {state[5]:.{sigfigs}}] m/s\n")

def kep_elem(name, kep, sigfigs=6):
    print(f"{name} Keplerian Elements:")
    print(f"Semimajor Axis (a): {kep[0]:.{sigfigs}} m")
    print(f"Eccentricity (e): {kep[1]:.{sigfigs}}")
    print(f"Inclination (i): {np.degrees(kep[2]):.{sigfigs}}º")
    print(f"RAAN (Ω): {np.degrees(kep[3]):.{sigfigs}}º")
    print(f"Argument of Periapse (𝜔): {np.degrees(kep[4]):.{sigfigs}}º")
    print(f"True Anomaly (f): {np.degrees(kep[5]):.{sigfigs}}º\n")

def show_body(fig, body, pos=np.array([0,0,0])):
    theta = np.linspace(0, 2.*np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    x = body.radius/1000 * np.outer(np.cos(theta), np.sin(phi)) + pos[0]
    y = body.radius/1000 * np.outer(np.sin(theta), np.sin(phi)) + pos[1]
    z = body.radius/1000 * np.outer(np.ones(np.size(theta)), np.cos(phi)) + pos[2]
    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=1.0, colorscale=body.colors, showscale=False))

def solar_system(t_array, spacecraft, bodies, show_sun=True):
    fig = go.Figure();  
    for i in range(len(bodies)):
        if show_sun or bodies[i].name != "Sun":
            x_au = np.array(convert.meters_to_AU(bodies[i].states[0,:]))
            y_au = np.array(convert.meters_to_AU(bodies[i].states[1,:]))
            z_au = np.array(convert.meters_to_AU(bodies[i].states[2,:]))
            fig.add_trace(go.Scatter3d(x=x_au, y=y_au, z=z_au, mode="lines",
                                    line=dict(width=4, color=t_array)))
    for sc in spacecraft:
        x_au = np.array(convert.km_to_AU(np.array(sc.history["state_x"])))
        y_au = np.array(convert.km_to_AU(np.array(sc.history["state_y"])))
        z_au = np.array(convert.km_to_AU(np.array(sc.history["state_z"])))
        fig.add_trace(go.Scatter3d(x=x_au, y=y_au, z=z_au, mode="lines",
                                   line=dict(width=4, color=t_array, colorscale=sc.colorscale), name=sc.name))
    fig.update_layout(
        title="Solar System",
        scene = dict(
            xaxis_title='X [AU]',
            yaxis_title='Y [AU]',
            zaxis_title='Z [AU]'),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.show()


def BCI(t_array, spacecraft, bodies):
    fig = go.Figure();  
    show_body(fig, bodies[0])
    for sc in spacecraft:
        fig.add_trace(go.Scatter3d(x=sc.history["state_x_bci"], y=sc.history["state_y_bci"], z=sc.history["state_z_bci"], mode="lines",
                                   line=dict(width=4, color=t_array, colorscale=sc.colorscale), name=sc.name))
    fig.update_layout(
        title="ECI Trajectory",
        scene = dict(
            xaxis_title='X [km]',
            yaxis_title='Y [km]',
            zaxis_title='Z [km]'),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.show()

def ECEF(t_array, spacecraft, bodies):
    if bodies[0].name != "Earth":
        print(f"{bodies[0].name} Centered {bodies[0].name} Fixed Trajectories not supported yet")
        return
    fig = go.Figure();  
    show_body(fig, bodies[0])
    for sc in spacecraft:
        fig.add_trace(go.Scatter3d(x=sc.history["state_x_ecef"], y=sc.history["state_y_ecef"], z=sc.history["state_z_ecef"], mode="lines",
                                   line=dict(width=4, color=t_array, colorscale=sc.colorscale), name=sc.name))
    fig.update_layout(
        title="ECEF Trajectory",
        scene = dict(
            xaxis_title='X [km]',
            yaxis_title='Y [km]',
            zaxis_title='Z [km]'),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.show()

def ground_track(t_array, spacecraft, bodies):
    if bodies[0].name == "Earth":
        coastline = np.loadtxt("GroundMaps/Earth.txt")
    else:
        print(f"Ground Track Not Supported for {bodies[0].name}")
        return
    
    latitudes = np.linspace(-89.99, 89.99, 360)
    longitudes = np.linspace(-179.99, 179.99, 720)
    illumination = np.zeros((len(latitudes), len(longitudes)))
    time = t_array[-1]
    z3 = np.zeros(3)
    earth_state = bodies[0].state
    for i in range(len(latitudes)):
        for j in range(len(longitudes)):
            eci_state = convert.ecef2eci(np.concatenate((convert.lla2ecef(np.array([latitudes[i], longitudes[j], 11000])), z3)), time)
            illumination[i,j] = dyn.total_illumination(convert.eci2icrs(eci_state, earth_state), bodies)

    fig = go.Figure();  
    fig.add_trace(go.Contour(z=illumination, line_smoothing=0, showscale=False, x=longitudes, y=latitudes, colorscale='gray', contours_coloring='heatmap', line=dict(width=0),
                             contours=dict(start=.01, end=1.0, size=0.1)))
    fig.add_trace(go.Scatter(x=coastline[:,0], y=coastline[:,1], mode="lines", line=dict(color='rgb(52, 165, 111)'), name=""))
    for sc in spacecraft:
        fig.add_trace(go.Scatter(x=sc.history["state_lon"], y=sc.history["state_lat"], mode="markers", 
                                 marker=dict(size=4, color=t_array, colorscale=sc.colorscale), name=sc.name))
    fig.update_layout(
    title="Ground Track",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
        )
    )
    fig.update_xaxes(range = [-180,180])
    fig.update_yaxes(range = [-90,90])
    fig.show()

def power_avail(t_array, spacecraft):
    fig = go.Figure();  
    for sc in spacecraft:
        fig.add_trace(go.Scatter(x=(t_array - t_array[0])*(24*60), y=np.array(sc.history["power_avail"])/1000, mode="lines", 
                                 marker=dict(size=4, color=t_array, colorscale=sc.colorscale), name=sc.name))
    fig.update_layout(
        title="Power Available",
        xaxis_title='Time [min]',
        yaxis_title='Power [kW]',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ))
    fig.show()