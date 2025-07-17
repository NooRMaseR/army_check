const ipc = document.getElementById("ipc").textContent;
const socket = new WebSocket(`ws://${ipc}:8000/ws/`);
const tableBody = document.getElementById("table-body");
const searchInput = document.getElementById("search");
const errorP = document.getElementById("error-msg");
const users = [];

socket.onmessage = (e) => {
  const data = JSON.parse(e.data);

  switch (data.type) {
    case "send.request": {
      tableBody.innerHTML += createRow(data);
      users.push({
        code: data.code,
        name: data.name,
        rank: data.rank,
        branch: data.branch,
        request: { accepted: data.request.accepted },
      });
      break;
    }

    case "send.pre.request": {
      const index = users.findIndex((v) => v.code === data.code);
      users[index].request = data.request;

      const element = document.querySelector(
        `[data-id='${data.code}'] td:nth-child(5)`
      );
      element.style.backgroundColor = "yellow";
      element.style.color = "black";
      element.textContent = data.request.accepted;
      break;
    }

    case "send.delete.request": {
      const index = users.findIndex((v) => v.code === data.code);
      users.splice(index, 1);
      document.querySelector(`[data-id='${data.code}']`).remove();
      break;
    }

    case "send.request.error": {
      errorP.textContent = data.message;
      setTimeout(() => (errorP.textContent = null), 5000);
      break;
    }

    case "accepted.action": {
      const index = users.findIndex((v) => v.code === data.code);
      users[index].request.accepted = "موافق";

      createSound(true);
      const element = document.querySelector(
        `[data-id='${data.code}'] td:nth-child(5)`
      );
      element.style.backgroundColor = "green";
      element.style.color = "white";
      element.textContent = "موافق";
      break;
    }

    case "denied.action": {
      const index = users.findIndex((v) => v.code === data.code);
      users[index].request.accepted = "تم الرفض";

      createSound(false);
      const element = document.querySelector(
        `[data-id='${data.code}'] td:nth-child(5)`
      );
      element.style.backgroundColor = "red";
      element.style.color = "white";
      element.textContent = "تم الرفض";
      break;
    }
  }
};

for (let userIndex = 0; userIndex < tableBody.children.length; userIndex++) {
  const currentRow = tableBody.children[userIndex].children;

  users.push({
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
          ${
            data.request.accepted === "انتظار"
              ? `<td style="background-color: yellow; color: black;">
            ${data.request.accepted}
          </td>`
              : data.request.accepted === "موافق"
              ? `
          <td style="background-color: green; color: white;">
            ${data.request.accepted}
          </td>`
              : `<td style="background-color: red; color: white;">
            ${data.request.accepted}
          </td>`
          }
          <td class="operations">
            <button class="send-pre-req" onclick="sendPreRequest('${data.code}');">ارسال طلب</button>
          </td>
        </tr>
        `;
}

async function createSound(accepted) {
  if (accepted) {
    const audio = new Audio("/static/acceptation.mp3");
    await audio.play();
  } else {
    const audio = new Audio("/static/denied.mp3");
    await audio.play();
  }
}

function sendRequest() {
  const name = document.getElementById("name");
  const rank = document.getElementById("rank");
  const code = document.getElementById("code");
  const branch = document.getElementById("branch");

  socket.send(
    JSON.stringify({
      type: "request",
      name: name.value,
      rank: rank.value,
      code: code.value,
      branch: branch.value,
    })
  );

  name.value = null;
  rank.value = null;
  code.value = null;
  branch.value = null;
}

function sendPreRequest(code) {
  const found = users.find((v) => v.code === code);
  socket.send(
    JSON.stringify({
      type: "pre_request",
      name: found.name,
      rank: found.rank,
      code: found.code,
      branch: found.branch,
    })
  );
}

function search() {
  tableBody.innerHTML = null;
  const foundData = users.find((v) => v.code.toLowerCase() === searchInput.value.toLowerCase());
  tableBody.innerHTML = createRow(foundData);
}

function reset() {
  tableBody.innerHTML = null;
  for (let i = 0; i < users.length; i++) {
    tableBody.innerHTML += createRow(users[i]);
  }
}
