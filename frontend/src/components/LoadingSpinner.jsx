/**
 * Loading spinner component with status messages.
 */
import React, { useState, useEffect } from 'react';

const LOADING_MESSAGES = [
    'Analyzing text...',
    'Classifying content...',
    'Detecting tone...',
    'Generating summary...',
];

export const LoadingSpinner = () => {
    const [messageIndex, setMessageIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setMessageIndex((prev) => (prev + 1) % LOADING_MESSAGES.length);
        }, 2000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="loading-spinner">
            <div className="spinner"></div>
            <p>{LOADING_MESSAGES[messageIndex]}</p>
        </div>
    );
};
