import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.graph_objects as go


nln = "\n"

DEFAULT_PLOTLY_COLORS=[
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    # '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]
from itertools import cycle
color_iter = cycle(DEFAULT_PLOTLY_COLORS)


def print_modes(modes, Tn=None, zeta=None, sigfigs=4):

    if len(modes) == 0:
        print("No valid identified modes.")
        return

    header = "       T(s)        \N{Greek Small Letter Zeta}        EMACO      MPC       EMACO*MPC"

    if Tn is not None:
        header += "     T % error"

    if zeta is not None:
        header += "    \N{Greek Small Letter Zeta} % error"

    print("Spectral quantities:")
    print(f"{header}")
    for mode in sorted(modes.values(), key=lambda x: x["freq"]):
        f = mode["freq"]
        z = mode["damp"]
        emaco = mode["energy_condensed_emaco"]
        mpc = mode["mpc"]
        row = f"      {1/f: <9.{sigfigs}}  {z: <9.{sigfigs}}  {emaco: <9.{sigfigs}}  {mpc: <9.{sigfigs}}  {emaco*mpc: <9.{sigfigs}}"
        if Tn is not None:
            row += f"    {100*(1/f-Tn)/(Tn): <9.{sigfigs}}"
        if zeta is not None:
            row += f"    {100*(z-zeta)/zeta: <9.{sigfigs}}"
        print(row)
    print("Mean Period(s):", np.mean([1/v["freq"] for v in modes.values()]))
    print("Standard Dev(s):", np.std([1/v["freq"] for v in modes.values()]))


def plot_models(models, Tn, zeta):
    # fig, ax = plt.subplots(2, 3, constrained_layout=True, sharex=True, figsize=(13,6.5))
    fig, ax = plt.subplots(2, 2, constrained_layout=True, sharex=True, figsize=(9,5))

    period = [models[method]["period"][0] for method in models]
    period_errors = [100*(p-Tn)/Tn for p in period]
    damp = [models[method]["damping"][0] for method in models]
    damping_errors = [100*(d-zeta)/zeta for d in damp]

    ax[0,0].bar(["true"]+[method.upper() for method in models.keys()], [Tn]+period)
    ax[0,0].set_title("Natural Period", fontsize=16)
    ax[0,0].set_ylabel("Period (s)", fontsize=14)

    ax[1,0].bar([method.upper() for method in models.keys()], period_errors, color=None, edgecolor="k", linewidth=0.5)
    ax[1,0].set_title("Period Errors", fontsize=16)
    ax[1,0].set_ylabel(r"Percent Error (\%)", fontsize=14)
    ax[1,0].set_xlabel("Method", fontsize=14)
    ax[1,0].set_xticklabels(["true"]+[method.upper() for method in models.keys()], rotation = 30)

    ax[0,1].bar(["true"]+[method.upper() for method in models.keys()], [zeta]+damp)
    ax[0,1].set_title("Damping", fontsize=16)
    ax[0,1].set_ylabel("Damping Ratio", fontsize=14)

    ax[1,1].bar([method.upper() for method in models.keys()], damping_errors, color=None, edgecolor="k", linewidth=0.5)
    ax[1,1].set_title("Damping Errors", fontsize=16)
    ax[1,1].set_ylabel(r"Percent Error (\%)", fontsize=14)
    ax[1,1].set_xlabel("Method", fontsize=14)
    ax[1,1].set_xticklabels(["true"]+[method.upper() for method in models.keys()], rotation = 30)

    for axi in ax.flatten():
        axi.grid(visible=True, which='both', axis='y')

    # ax[0,2].axis('off')

    # times_list = [models[method]["time"] for method in models]
    # ax[1,2].bar(models.keys(), times_list, color=None, edgecolor="k", linewidth=0.5)
    # ax[1,2].set_title("Runtime")# , fontsize=14)
    # ax[1,2].set_ylabel("time (s)")# , fontsize=13)
    # ax[1,2].set_xlabel("Method")# , fontsize=13)

    # # for i,error in enumerate([period_errors,damping_errors,times_list]):
    # for i,error in enumerate([period_errors,damping_errors]):
    #     rects = ax[1,i].patches
    #     for rect, label in zip(rects, error):
    #         label = f"{label: <5.3}"
    #         height = rect.get_height()
    #         ax[1,i].text(
    #             rect.get_x() + rect.get_width() / 2, height, label, ha="center", va="bottom"
    #         )
    
    # fig.suptitle("Spectral Quantity Prediction with System Identification",fontsize=17)


def plot_io(inputs, outputs, t, title=None, xlabels=("time (s)", "time (s)"), ylabels=("inputs","outputs"), axtitles=(None,None), **options):
    fig, ax = options.get('figax',
                          plt.subplots(1,2,figsize=options.get('figsize',(10,3)),constrained_layout=True,sharey=options.get('sharey',(ylabels[0]==ylabels[1])))
    )
    if len(inputs.shape) > 1:
        for i in range(inputs.shape[0]):
            ax[0].plot(t,inputs[i,:],label=f"input {i+1}")
    else:
        ax[0].plot(t,inputs)
    ax[0].set_xlabel(xlabels[0], fontsize=15)
    ax[0].set_ylabel(ylabels[0], fontsize=15)
    ax[0].set_title(axtitles[0], fontsize=15)
    if len(outputs.shape) > 1:
        for i in range(outputs.shape[0]):
            ax[1].plot(t,outputs[i,:],alpha=0.5,label=f"output {i+1}")
        ax[1].legend(fontsize=12, frameon=True, framealpha=0.4, bbox_to_anchor=(1,0,0.5,0.8), loc='upper left')
    else:
        ax[1].plot(t,outputs)
    ax[1].set_xlabel(xlabels[1], fontsize=15)
    ax[1].set_ylabel(ylabels[1], fontsize=15)
    ax[1].set_title(axtitles[1], fontsize=15)
    fig.suptitle(title, fontsize=17)
    return fig


def plot_pred(ytrue, models, t, title=None, xlabel="time (s)", ylabel="outputs", makelegend=True, **options):
    linestyles = ['dashed', 'dashdot', 'dotted']
    colors = ['blue', 'orange', 'green', 'magenta']
    true_first = options['true_first'] if 'true_first' in options.keys() else False
    true_label = options.get('true_label','true')
    model_label = options.get('model_label','prediction')

    # fig, ax = options.get('figax',plt.subplots(figsize=options.get('figsize',(6,3))))
    fig, ax = options['figax'] if 'figax' in options.keys() else plt.subplots(figsize=options.get('figsize',(6,3)))
    if true_first:
        if len(ytrue.shape) > 1:
            for i in range(ytrue.shape[0]):
                ax.plot(t,ytrue[i,:],label=f"true, DOF {i+1}",color='black',alpha=0.5,linestyle=linestyles[i%len(linestyles)])
        else:
            ax.plot(t,ytrue,label=true_label,color='black',alpha=0.5)
    if type(models) is np.ndarray:
        if len(models.shape) > 1:
            for i in range(models.shape[0]):
                ax.plot(t,models[i,:],label=f"{model_label}, DOF {i+1}" if models.shape[0]>1 else f"{options.get('single_label',model_label)}",
                        linestyle=linestyles[i%len(linestyles)],linewidth=2,color=options.get('single_color',colors[i%len(colors)]),alpha=0.5)
        else:
            ax.plot(t,models,"--",color=options.get('single_color',None),label=f"{options.get('single_label',model_label)}")
    else:
        for k,method in enumerate(models):
            if len(models[method]["ypred"].shape) > 1:
                for i in range(models[method]["ypred"].shape[0]):
                    ax.plot(t,models[method]["ypred"][i,:],
                            linestyle=linestyles[i%len(linestyles)],linewidth=2,color=colors[k],alpha=0.5,
                            label=f"{method.upper()}, DOF {i+1}" if models[method]["ypred"].shape[0]>1 else f"{method.upper()}")
            else:
                ax.plot(t,models[method]["ypred"],linestyle=linestyles[k%len(linestyles)],linewidth=2,color=colors[k],alpha=0.5,label=method.upper())
    if not true_first:
        if len(ytrue.shape) > 1:
            for i in range(ytrue.shape[0]):
                ax.plot(t,ytrue[i,:],label=f"true, DOF {i+1}",color='black',alpha=0.5,linestyle=linestyles[i%len(linestyles)])
        else:
            ax.plot(t,ytrue,label=true_label,color='black',alpha=0.5)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    min_y = options.get('min_y',None)
    max_y = options.get('max_y',None)
    ax.set_ylim((min_y,max_y))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    if min_y is not None and max_y is not None:
        if np.max([abs(min_y),max_y]) < 0.05:
            base = 0.02
        elif np.max([abs(min_y),max_y]) < 0.1:
            base = 0.05
        elif np.max([abs(min_y),max_y]) < 0.5:
            base = 0.2
        elif np.max([abs(min_y),max_y]) < 2.0:
            base = 0.5
        else:
            base = 1.0
        ax.yaxis.set_major_locator(ticker.MultipleLocator(base=base))
    ax.yaxis.minorticks_off()
    # ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)
    if makelegend:
        fig.legend(fontsize=12, frameon=True, framealpha=0.4, bbox_to_anchor=(0.9,0,0.5,0.8), loc='upper left')    
    fig.suptitle(title, fontsize=14)
    return fig


def plot_transfer(models, title=None, labels=None, plotly=False, **options):
    if plotly:
        import plotly.graph_objects as go
        layout = go.Layout(
            title=title,
            xaxis=dict(
                title="Period (s)"
            ),
            yaxis=dict(
                title=options.get('ylabel', "Amplitude")
            ),
            width=600, height=300,
            margin=dict(l=70, r=20, t=20, b=20))
        fig = go.Figure(layout=layout)
        if type(models) is np.ndarray:
            if len(models.shape) > 2:
                for i in range(models.shape[0]):
                    fig.add_trace(go.Scatter(x=models[i,0],y=models[i,1]/max(models[i,1]),name=labels[i] if labels is not None else None))
            else:
                fig.add_trace(go.Scatter(x=models[0],y=models[1]/max(models[1]),name=labels))
        else:
            for method in models:
                fig.add_trace(go.Scatter(x=models[method][0],y=models[method][1]/max(models[method][1]),name=method))
        fig.show(renderer="notebook_connected")
    else:
        linestyles = ['-','--',':']
        fig, ax = plt.subplots(figsize=options.get('figsize',(6,3)))
        if type(models) is np.ndarray:
            if len(models.shape) > 2:
                for i in range(models.shape[0]):
                    ax.plot(models[i,0],models[i,1]/max(models[i,1]),linestyle=linestyles[i],label=labels[i] if labels is not None else None)
            else:
                ax.plot(models[0],models[1]/max(models[1]),label=labels)
        else:
            for i,method in enumerate(models):
                ax.plot(models[method][0],models[method][1]/max(models[method][1]),linestyle=linestyles[i],label=method)
        ax.set_xlabel("Period (s)",fontsize=14)
        ax.set_ylabel(options.get('ylabel', "Amplitude"),fontsize=14)
        if (labels is not None) or (not type(models) is np.ndarray):
            ax.legend(fontsize=12, frameon=True, framealpha=0.4, bbox_to_anchor=(1,0,0.5,0.8), loc='upper left')
        ax.set_title(title)
        return fig


def make_hover_data(data, ln=None):
    import numpy as np
    if ln is None:
        items = np.array([d.values for d in data])
        keys = data[0].keys()
    else:
        items = np.array([list(data.values())]*ln)
        keys = data.keys()
    return {
        "hovertemplate": "<br>".join(f"{k}: %{{customdata[{v}]}}" for v,k in enumerate(keys)),
        "customdata": list(items),
    }


def plot_fdd(outputs, dt, true_periods=None):
    from mdof import transform, modal
    ndof = outputs.shape[0]
    fdd_freq,U,S = transform.fdd(outputs=outputs, step=dt)
    identified_periods = np.empty(ndof)

    from scipy.signal import find_peaks
    _,ax = plt.subplots(figsize=(7,3))
    for j in range(ndof):
        amplitudes = S[j,:]
        amplitudes = amplitudes/max(amplitudes)
        peaks, _ = find_peaks(amplitudes, prominence=0.3)        
        _, fundamental_amps = modal.spectrum_modes(fdd_freq, amplitudes)
        if true_periods is not None:
            ax.axvline(periods[j], color="k", label="original periods" if j==0 else None)
        ax.plot(1/fdd_freq, amplitudes)
        identified_periods[j] = 1/(fdd_freq[peaks[0]])
        if j==0:
            identified_modeshapes = U[:,:,peaks[0]]
        ax.scatter(identified_periods[j], fundamental_amps[0], label=f"identified period {j+1}")
    if true_periods is not None:
        ax.set_xlim([0, np.max(periods)*2])
    else:
        ax.set_xlim([0, np.max(identified_periods)*2])
    ax.set_xlabel("Period (s)")
    ax.set_ylabel("Amplitude")
    ax.legend(fontsize=12, frameon=True, framealpha=1) 

    return identified_periods, identified_modeshapes

def plotly_windowed_transfer(inputs, outputs, dt, method='fourier', normalize=True):
    _,_,_,time = create_time_vector(inputs.shape[1],dt)
    time_grid, period_grid, amplitude_grid = moving_window_transfer(time,
                                                                    inputs,
                                                                    outputs,
                                                                    method=method,
                                                                    normalize=normalize)
    fig = plot_moving_window(time_grid, period_grid, amplitude_grid, plotly=True)
    return fig


if __name__ == "__main__":

    import numpy as np
    periods = np.array([0.1,0.3,0.5,0.7])
    amplitudes = np.array([0.1,0.2,1,0.2])

    plot = FrequencyContent(scale=True, period=True, xlabel="Period (s)", ylabel="Amplitude")

    plot.add(periods, amplitudes, label="R1")
    plot.add(periods[:2], label="SRIM")
    plot.add(periods[2:], label="SRIM")
    plot.add(periods, amplitudes-0.05, label="R1")

    fig:go.Figure = plot.get_figure()
    print(fig.to_json())