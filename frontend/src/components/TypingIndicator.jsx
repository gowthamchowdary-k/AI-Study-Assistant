import { motion } from "framer-motion";

const dotAnimation = {
    animate: {
        y: [0, -6, 0]
    }
};

const transition = {
    duration: 0.6,
    repeat: Infinity
};

export default function TypingIndicator() {

    return (

        <div className="flex justify-start mb-6">

            <div
                className="
                    bg-white
                    border
                    border-gray-200
                    rounded-2xl
                    rounded-bl-md
                    shadow-md
                    px-5
                    py-4
                "
            >

                <div className="flex items-center gap-2">

                    <motion.div
                        variants={dotAnimation}
                        animate="animate"
                        transition={{
                            ...transition,
                            delay: 0
                        }}
                        className="w-2.5 h-2.5 rounded-full bg-blue-500"
                    />

                    <motion.div
                        variants={dotAnimation}
                        animate="animate"
                        transition={{
                            ...transition,
                            delay: 0.2
                        }}
                        className="w-2.5 h-2.5 rounded-full bg-blue-500"
                    />

                    <motion.div
                        variants={dotAnimation}
                        animate="animate"
                        transition={{
                            ...transition,
                            delay: 0.4
                        }}
                        className="w-2.5 h-2.5 rounded-full bg-blue-500"
                    />

                </div>

            </div>

        </div>

    );

}