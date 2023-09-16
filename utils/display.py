import numpy as np
import plotly.graph_objects as go

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

def show_central_body(fig, central_body):
    theta = np.linspace(0, 2.*np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    x = central_body.radius * np.outer(np.cos(theta), np.sin(phi))
    y = central_body.radius * np.outer(np.sin(theta), np.sin(phi))
    z = central_body.radius * np.outer(np.ones(np.size(theta)), np.cos(phi))
    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=1.0, colorscale= central_body.colors, showscale=False))

def BCI(t_array, trajs, names, colorscales, central_body):
    fig = go.Figure();  
    show_central_body(fig, central_body)
    for i in range(len(trajs)):
        fig.add_trace(go.Scatter3d(x=trajs[names[i]]["state_x_eci"], y=trajs[names[i]]["state_y_eci"], z=trajs[names[i]]["state_z_eci"], mode="lines",
                                   line=dict(width=4, color=t_array, colorscale=colorscales[i]), name=names[i]))
    fig.update_layout(
        title="ECI Trajectory",
        scene = dict(
            xaxis_title='X [m]',
            yaxis_title='Y [m]',
            zaxis_title='Z [m]'),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.show()

def ECEF(t_array, trajs, names, colorscales, central_body):
    if central_body.name != "Earth":
        print(f"{central_body.name} Centered {central_body.name} Fixed Trajectories not supported yet")
        return
    fig = go.Figure();  
    show_central_body(fig, central_body)
    for i in range(len(trajs)):
        fig.add_trace(go.Scatter3d(x=trajs[names[i]]["state_x_ecef"], y=trajs[names[i]]["state_y_ecef"], z=trajs[names[i]]["state_z_ecef"], mode="lines",
                                   line=dict(width=4, color=t_array, colorscale=colorscales[i]), name=names[i]))
    fig.update_layout(
        title="ECEF Trajectory",
        scene = dict(
            xaxis_title='X [m]',
            yaxis_title='Y [m]',
            zaxis_title='Z [m]'),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.show()

def ground_track(t_array, trajs, names, colorscales, central_body):
    if central_body.name == "Earth":
        coastline = np.loadtxt("GroundMaps/Earth.txt")
    else:
        print("Ground Track Not Supported for {central_body.name}}")
        return
    fig = go.Figure();  
    fig.add_trace(go.Scatter(x=coastline[:,0], y=coastline[:,1], mode="lines", line=dict(color='rgb(52, 165, 111)'), name=""))
    for i in range(len(trajs)):
        fig.add_trace(go.Scatter(x=trajs[names[i]]["state_lon"], y=trajs[names[i]]["state_lat"], mode="markers", 
                                 marker=dict(size=4, color=t_array, colorscale=colorscales[i], opacity=1), name=names[i]))
    fig.update_layout(
    title="Ground Track",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
        )
    )
    fig.show()

