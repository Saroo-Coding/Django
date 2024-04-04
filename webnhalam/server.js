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
    socket.on('joinRoom', (item) => {
        const room = rooms[item.link] || [];
        if (room.length === 2) {
            socket.emit('roomFull', 'full');
        } else {
            room.push({ uId: item.uId });
            rooms[item.link] = room;
            socket.join(item.link);
            io.to(item.link).emit('roomFull', room.length);
            socket.uId = item.uId;
            socket.link = item.link;
        }
    });

    // Tham gia vào room ngẫu nhiên
    socket.on('joinRandomRoom', () => {
        // Lấy danh sách các room
        const availableRooms = Object.keys(rooms);

        // Chọn ngẫu nhiên một room từ danh sách
        const randomRoomIndex = Math.floor(Math.random() * availableRooms.length);
        const randomRoom = availableRooms[randomRoomIndex];

        socket.join(randomRoom);

        // Gửi sự kiện 'roomJoined' với tên room đến client
        socket.emit('roomJoined', randomRoom);
    });

    // Lắng nghe sự kiện chọn
    socket.on('seclect', (item) => {
        io.to(item.link).emit('opponent', item.uId);
        if (moves[item.link] !== undefined) {
            moves[item.link].push({uId: item.uId,move: item.item})//player 2
        }
        else{
            moves[item.link] = [{ uId: item.uId, move: item.item }] //player 1
        }
        if (moves[item.link] && moves[item.link].length === 2) {
            calculateResult(moves[item.link][0].move, moves[item.link][1].move, moves[item.link][0].uId, moves[item.link][1].uId, item.link)
        }
    });

    //game play 
    function calculateResult(move1, move2, uId1, uId2, link) {
        if (move1 === move2) {
            io.to(link).emit('result', {win:'tie',lose:'tie'});
            // It's a tie!
        } else if ((move1 === 'rock' && move2 === 'scissors') ||
            (move1 === 'paper' && move2 === 'rock') ||
            (move1 === 'scissors' && move2 === 'paper')) {
            io.to(link).emit('result', {win:uId1,lose:uId2});
            // Player 1 wins!
        } else {
            io.to(link).emit('result', {win:uId2,lose:uId1});
            // Player 2 wins!
        }
    }

    //Winner
    socket.on('winner',(item) => {
        console.log('win 3* là: ' + item.uId)
    });

    //next round
    socket.on('nextRound',(item) => {
        moves[item] = [];
    });

    // Giảm số lượng người trong phòng khi máy khách ngắt kết nối ngắt kết nối
    socket.on('disconnect', () => {
        console.log('Một máy khách đã ngắt kết nối');
        if (rooms[socket.link] && rooms[socket.link].length > 0) { //Check 
            if (rooms[socket.link].some(item => item.uId === socket.id)) {
                rooms[socket.link] = rooms[socket.link].filter(item => item.uId !== socket.uId);//bớt người
                moves[socket.link] = []; //reset chọn
                if (rooms[socket.link].length === 0) {
                    delete rooms[socket.link];
                    delete moves[socket.link];
                    io.to(socket.link).emit('userLeave', 0);
                }
                else
                    io.to(socket.link).emit('userLeave', rooms[socket.link].length);
            }
        }
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Máy chủ Socket.IO đang chạy tại cổng ${PORT}`);
});
