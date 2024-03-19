import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.parasite_axes import HostAxes


st.set_page_config(layout='wide')
# 設置中文字體
plt.rcParams['font.family'] = ['Microsoft JhengHei']


def custom_placeholder(text, color):
    return st.markdown(f'<div style="padding: 150px; background-color: #808080; border-radius: 5px;">{text}</div>', unsafe_allow_html=True)

def run():

    st.title("折線圖")
    
    st.sidebar.title("選擇顯示的折線")


    placeholder = custom_placeholder(" "," ")
    
    # 上傳CSV檔案
    uploaded_file = st.file_uploader("選擇一個CSV檔案", type=["csv"])

    if uploaded_file is not None:
        # 將上傳的檔案轉換為big5編碼(有中文)
        df = pd.read_csv(uploaded_file, encoding='utf-8', index_col=0)


        # 資料整理
        unit = df.pop('Unit/Time')

        # 去除非數值類row
        to_discard = unit[unit.values == 'V'].index.values
        df.drop(to_discard, inplace=True)
        df.dropna(inplace=True, how='all')
        df.fillna(0, inplace=True)
        df = df.astype('float')
        
        # # 第一行中文作為X軸的刻度
        # x_labels = list(df.columns)

        # 繪製折線圖
        options = list(df.index)
        # 第二行當做預設
        default_selected_lines = [options[0]]

        # 繪製折線圖
        if options:
            selected_lines = st.sidebar.multiselect("select_data", options, default=default_selected_lines, label_visibility='hidden')

            # Plotting by matplotlib
            if selected_lines:
                fig = plt.figure(figsize=(20, 5))
                host = fig.add_axes((0.15, 0.1, 0.65, 0.8), axes_class=HostAxes)
                # Set each y-axis's location
                ylocation = [x_site * -50 for x_site in range(len(selected_lines))]


                # Draw main plot in "host" and other plot in psub
                for i in range(len(selected_lines)):
                    if i == 0:
                        host_values = df.loc[selected_lines[i]]
                        phost, = host.plot(host_values, label=selected_lines[i])
                        host.set(ylim=(min(host_values) - 1, max(host_values) + 1), ylabel=selected_lines[i])
                    else:
                        sub_values = df.loc[selected_lines[i]]
                        psub = host.get_aux_axes(viewlim_mode=None, sharex=host)
                        psub.axis["left"] = psub.new_fixed_axis(loc="left", offset=(ylocation[i], 0))
                        sub,  = psub.plot(sub_values, label=selected_lines[i])
                        psub.set(ylim=(min(sub_values) - 1, max(sub_values) + 1),  ylabel=selected_lines[i])

                host.legend(loc=4)
                placeholder.pyplot(fig)

        else:
            st.warning("檔案沒有數據可供顯示")


if __name__ == "__main__":
    run()
