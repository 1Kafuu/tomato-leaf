"use client";

import { useState } from "react";

type AccordionProps = {
  title: string;
  content: string;
};

export default function Accordion({ title, content }: AccordionProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="rounded-2xl text-text-heading text-left border-2 border-border-default">
      <button
        className="w-full px-6 py-2 flex flex-col"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex flex-row justify-between items-center py-4 label-semibold">
          <span className="text-left pr-4">{title}</span>
          <svg
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`shrink-0 transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`}
          >
            <path
              d="M5 7.5L10 12.5L15 7.5"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        {isOpen && (
          <div className="text-text-label pb-4">
            <p className="sm-default leading-relaxed text-left">{content}</p>
          </div>
        )}
      </button>
    </div>
  );
}
