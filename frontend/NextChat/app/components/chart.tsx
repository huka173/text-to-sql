import React from "react";
import ReactECharts from "echarts-for-react";

export default function Chart(props: { code: string }) {
    const option = JSON.parse(props.code);
    return (
        <ReactECharts
            option={option}
            style={{
                width: "100%",
                height: 400,
            }}
        />
    );
}