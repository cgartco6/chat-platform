import React, { createContext, useContext, useEffect, useState } from 'react';
import io from 'socket.io-client';
import { useAuth } from './auth';
import { api } from './api';

const SocketContext = createContext();

export const useSocket = () => {
  return useContext(SocketContext);
};

export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      // Get the token from AsyncStorage
      const connectSocket = async () => {
        try {
          const token = await AsyncStorage.getItem('authToken');
          
          const newSocket = io(api.defaults.baseURL, {
            auth: {
              token: token
            }
          });

          newSocket.on('connect', () => {
            console.log('Connected to server');
          });

          newSocket.on('disconnect', () => {
            console.log('Disconnected from server');
          });

          setSocket(newSocket);

          return () => newSocket.close();
        } catch (error) {
          console.error('Socket connection error:', error);
        }
      };

      connectSocket();
    } else {
      if (socket) {
        socket.close();
        setSocket(null);
      }
    }
  }, [user]);

  return (
    <SocketContext.Provider value={socket}>
      {children}
    </SocketContext.Provider>
  );
};
