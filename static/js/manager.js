const ipc = document.getElementById("ipc").textContent;
const socket = new WebSocket(`ws://${ipc}:8000/ws/manager/`);
const tableBody = document.getElementById("table-body");
const errorP = document.getElementById("error-msg");
const requests = [];

for (let userIndex = 0; userIndex < tableBody.children.length; userIndex++) {
  const currentRow = tableBody.children[userIndex].children;

  requests.push({
    code: currentRow[0].textContent,
    name: currentRow[1].textContent,
    rank: currentRow[2].textContent,
    branch: currentRow[3].textContent,
    request: { accepted: currentRow[4].textContent.trim() },
  });
}

function createRow(data) {
  return `
        <tr data-id='${data.code}'>
          <td>${data.code}</td>
          <td>${data.name}</td>
          <td>${data.rank}</td>
          <td>${data.branch}</td>
          
        <td style="background-color: yellow; color: black;">
            ${data.request.accepted}
          </td>
          <td class="operations">
            <button class="send-accept" onclick="sendAcceptAction('${data.code}');">موافق</button>
            <button class="send-denied" onclick="sendDeniedAction('${data.code}');">رفض</button>
          </td>
        </tr>
        `;
}

socket.onmessage = (e) => {
  const data = JSON.parse(e.data);

  switch (data.type) {
    case "send.request": {
      tableBody.innerHTML += createRow(data);
      requests.push({
        code: data.code,
        name: data.name,
        rank: data.rank,
        branch: data.branch,
        request: { accepted: data.request.accepted },
      });
      break;
    }

    case "send.pre.request": {
      const index = requests.findIndex((v) => v.code === data.code);
      if (index === -1) {
        requests.push({
          code: data.code,
          name: data.name,
          rank: data.rank,
          branch: data.branch,
          request: { accepted: data.request.accepted },
        });
        tableBody.innerHTML += createRow(data);
      } else {
        requests[index].accepted = data.accepted;
        const element = document.querySelector(
          `[data-id='${data.code}'] td:nth-child(5)`
        );
        element.style.backgroundColor = "yellow";
        element.style.color = "black";
        element.textContent = "انتظار";
      }
      break;
    }

    case "accepted.action": {
      const index = requests.findIndex((v) => v.code === data.code);
      requests[index].request.accepted = "موافق";

      const element = document.querySelector(
        `[data-id='${data.code}'] td:nth-child(5)`
      );
      element.style.backgroundColor = "green";
      element.style.color = "white";
      element.textContent = "موافق";
      removeRow(data.code, index);
      break;
    }

    case "denied.action": {
      const index = requests.findIndex((v) => v.code === data.code);
      requests[index].request.accepted = "تم الرفض";

      const element = document.querySelector(
        `[data-id='${data.code}'] td:nth-child(5)`
      );
      element.style.backgroundColor = "red";
      element.style.color = "white";
      element.textContent = "تم الرفض";
      removeRow(data.code, index);
      break;
    }
  }
};

function sendAcceptAction(code) {
  socket.send(
    JSON.stringify({
      type: "accepted",
      code: code,
    })
  );
}

function sendDeniedAction(code) {
  socket.send(
    JSON.stringify({
      type: "denied",
      code: code,
    })
  );
}

function removeRow(code, index, timer = true) {
  if (timer) {
    setTimeout(() => {
      requests.splice(index, 1);
      document.querySelector(`[data-id='${code}']`).remove();
    }, 5000);
  } else {
    requests.splice(index, 1);
    document.querySelector(`[data-id='${code}']`).remove();
  }
}
