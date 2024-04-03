const http = require('http');
const { Server } = require('socket.io');

const server = http.createServer();
const io = new Server(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});
const rooms = {};
const moves = {};


io.on('connection', (socket) => {
    console.log('Một máy khách đã kết nối');
    // Lắng nghe sự kiện 'joinRoom' từ máy khách
    socket.on('joinRoom', (roomId) => {
        if (rooms[roomId] && rooms[roomId] === 2) {
            socket.emit('roomFull', 'full');//báo 
            return;
        }
        else {
            socket.join(roomId);
            rooms[roomId] = (rooms[roomId] || 0) + 1;
            io.to(roomId).emit('roomFull', rooms[roomId]);
        }
    });

    // Lắng nghe sự kiện từ các máy khách
    socket.on('seclect', (item) => {
        if (moves[item.link] !== undefined) {
            moves[item.link].push({uId: item.uId,move: item.item})
        }
        else{
            moves[item.link] = [{ uId: item.uId, move: item.item }]
        }
        if (moves[item.link] && moves[item.link].length === 2) {
            //console.log(moves[item.link][0].move)
            calculateResult(moves[item.link][0].move, moves[item.link][1].move, moves[item.link][0].uId, moves[item.link][1].uId, item.link)
        }
    });

    //game play 
    function calculateResult(move1, move2, uId1, uId2, link) {
        if (move1 === move2) {
            return "It's a tie!";
        } else if ((move1 === 'rock' && move2 === 'scissors') ||
            (move1 === 'paper' && move2 === 'rock') ||
            (move1 === 'scissors' && move2 === 'paper')) {
            io.to(link).emit('result', {win:uId1,lose:uId2});
            //return 'Player 1 wins!';
        } else {
            io.to(link).emit('result', {win:uId2,lose:uId1});
            //return 'Player 2 wins!';
        }
    }

    // Xử lý sự kiện ngắt kết nối
    socket.on('disconnect', () => {
        console.log('Một máy khách đã ngắt kết nối');
        // Giảm số lượng người trong phòng khi máy khách ngắt kết nối
        Object.keys(rooms).forEach((roomId) => {
            if (rooms.hasOwnProperty(roomId)) {
                rooms[roomId] -= 1;
                io.to(roomId).emit('userLeave', rooms[roomId]);
                if (rooms[roomId] <= 0) delete rooms[roomId]; // Xóa phòng nếu không có ai trong đó
                // Reset lựa chọn của người chơi
                delete moves[roomId];
            }
        });
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Máy chủ Socket.IO đang chạy tại cổng ${PORT}`);
});
