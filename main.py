from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd

app = FastAPI()

# CSV 파일 경로
csv_file_path = "data.csv"

@app.get("/data", response_class=JSONResponse)
async def get_data():
    df = pd.read_csv(csv_file_path)
    return df.to_dict(orient="records")

@app.get("/", response_class=HTMLResponse)
async def render_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Visualization</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
            }
            canvas {
                margin: 20px auto;
                display: block;
            }
            table {
                margin: 20px auto;
                border-collapse: collapse;
                width: 80%;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f4f4f4;
            }
        </style>
    </head>
    <body>
        <h1>데이터 시각화</h1>

        <canvas id="chart1" width="600" height="400"></canvas>
        <canvas id="chart2" width="600" height="400"></canvas>
        <canvas id="chart3" width="600" height="400"></canvas>

        <h2>데이터 테이블</h2>
        <div id="data-table"></div>

        <script>
            async function fetchData() {
                const response = await fetch('/data');
                const data = await response.json();

                // 데이터 열 이름 설정
                const labels = data.map(item => item['연도']); // 연도
                const accidents = data.map(item => parseInt(item['사고'], 10)); // 사고 건수
                const deaths = data.map(item => parseInt(item['사망'], 10)); // 사망자 수
                const injuries = data.map(item => parseInt(item['부상'], 10)); // 부상자 수

                // 첫 번째 그래프: 사고 건수
                const ctx1 = document.getElementById('chart1').getContext('2d');
                new Chart(ctx1, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: '사고 건수',
                                data: accidents,
                                borderColor: 'rgba(255, 99, 132, 1)',
                                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                fill: true
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'top' },
                            title: { display: true, text: '사고 건수' }
                        },
                        scales: { y: { beginAtZero: true } }
                    }
                });

                // 두 번째 그래프: 사망자 수
                const ctx2 = document.getElementById('chart2').getContext('2d');
                new Chart(ctx2, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: '사망자 수',
                                data: deaths,
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                borderColor: 'rgba(54, 162, 235, 1)',
                                borderWidth: 1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'top' },
                            title: { display: true, text: '사망자 수' }
                        },
                        scales: { y: { beginAtZero: true } }
                    }
                });

                // 세 번째 그래프: 부상자 수
                const ctx3 = document.getElementById('chart3').getContext('2d');
                new Chart(ctx3, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: '부상자 수',
                                data: injuries,
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                fill: true
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'top' },
                            title: { display: true, text: '부상자 수' }
                        },
                        scales: { y: { beginAtZero: true } }
                    }
                });

                // 데이터 테이블 생성
                const tableDiv = document.getElementById('data-table');
                let tableHTML = '<table><thead><tr>';

                // 테이블 헤더
                Object.keys(data[0]).forEach(key => {
                    tableHTML += `<th>${key}</th>`;
                });
                tableHTML += '</tr></thead><tbody>';

                // 테이블 데이터
                data.forEach(row => {
                    tableHTML += '<tr>';
                    Object.values(row).forEach(value => {
                        tableHTML += `<td>${value}</td>`;
                    });
                    tableHTML += '</tr>';
                });

                tableHTML += '</tbody></table>';
                tableDiv.innerHTML = tableHTML;
            }

            fetchData();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
