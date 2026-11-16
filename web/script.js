function fetchState() {
    fetch("/api/state")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // 局情報
            document.getElementById("round").textContent = data.round;
            document.getElementById("counters").textContent = data.counters;
            document.getElementById("deposit").textContent = data.deposit;

            // プレイヤー情報
            const seats = ["東", "南", "西", "北"];

            seats.forEach(seat => {
                const player = data.players[seat];

                const section = document.querySelector(
                    `.player[data-seat="${seat}"]`
                );

                section.querySelector('[data-field="diff"]').textContent =
                    player.diff.toLocaleString("ja-JP");

                section.querySelector('[data-field="tsumo"]').textContent =
                    player.tsumo;

                section.querySelector('[data-field="ron"]').textContent =
                    player.ron;
            });

            // ステータス表示
            const statusMessages = {
                ready: "ゲーム情報を確認済み",
                loading: "新しい局を確認中...",
                error: "ゲーム情報を確認できません",
            };

            const statusElement = document.getElementById("status");

            statusElement.textContent =
                statusMessages[data.status] ?? "状態を確認できません";

            statusElement.classList.toggle(
                "error",
                data.status === "error"
            );
        })
        .catch(error => {
            console.error("データ取得エラー:", error);

            const statusElement = document.getElementById("status");
            statusElement.textContent =
                "通信エラー：表示を更新できません";
            statusElement.classList.add("error");
        });
}

// ページを開いた直後に実行
fetchState();

// 3秒ごとに実行
setInterval(fetchState, 3000);