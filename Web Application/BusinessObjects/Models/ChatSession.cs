using System;
using System.Collections.Generic;

namespace BusinessObjects.Models;

public partial class ChatSession
{
    public int SessionId { get; set; }

    public int UserId { get; set; }

    public DateTime? StartedAt { get; set; }

    public DateTime? EndedAt { get; set; }

    public virtual ICollection<ChatMessage> ChatMessages { get; set; } = new List<ChatMessage>();

    public virtual User User { get; set; } = null!;
}
